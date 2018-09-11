#!/usr/bin/env python2

# https://github.com/mapnik/mapnik/wiki/UbuntuInstallation
# https://github.com/mapnik/python-mapnik
# export BOOST_PYTHON_LIB=boost_python
# python setup.py install --prefix=~/.local
# RUN apk add --no-cache python3
# pip install overpass

from mapnik import *
import gdal
import math
import shutil
from os.path import dirname, basename, splitext, join, exists
from spatialconv.conv import toSpatial
import os
import time

from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn
from Queue import Queue
import multiprocessing
from threading import Event, Lock
from collections import OrderedDict

OSM_MAX_RETRIES = 4
mapfile = 'mapnik.xml'
emptymapfile = 'empty-mapnik.xml'
emptymapstring = ''
emptydb = 'www/empty.spatialite'
emptyosm = 'www/empty.osm'
DB_REPLACE = 'test_db4.sqlite'
dbFormat = 'www/{}/{}/{}.spatialite'
osmFormat = 'www/{}/{}/{}-{}.osm'

datasources = {
    'roads': '''
    (
        way[highway];
    );
    ''',
    'railway': '''
    (
        way[railway];
    );
    ''',
    'leisure': '''
    (
        way[leisure];
    );
    ''',
    'landuse': '''
    (
        way[landuse];
    );
    ''',
    'places': '''
    (
        node[place];
    );
    ''',
    'natural': '''
    (
        way[natural][natural!~'(water)|(lake)|(land)|(glacier)|(mud)|(marsh)|(wetland)'];
        rel[natural][natural!~'(water)|(lake)|(land)|(glacier)|(mud)|(marsh)|(wetland)'];
    );
    ''',
    'building': '''
    (
        way[building];rel[building];
    );
    ''',
    'water': '''
    (
        node[water];  way[water];  rel[water];
        node[waterway];  way[waterway];  rel[waterway];
        node["landuse"="reservoir"];  way["landuse"="reservoir"];  rel["landuse"="reservoir"];
        node["landuse"="water"];  way["landuse"="water"];  rel["landuse"="water"];
        node["landuse"="basin"];  way["landuse"="basin"];  rel["landuse"="basin"];
        node["natural"="lake"];  way["natural"="lake"];  rel["natural"="lake"];
        node["natural"="water"];  way["natural"="water"];  rel["natural"="water"];
        node["natural"="land"];  way["natural"="land"];  rel["natural"="land"];
        node["natural"="glacier"];  way["natural"="glacier"];  rel["natural"="glacier"];
        node["natural"="mud"];  way["natural"="mud"];  rel["natural"="mud"];
        node["natural"="marsh"];  way["natural"="marsh"];  rel["natural"="marsh"];
        node["natural"="wetland"];  way["natural"="wetland"];  rel["natural"="wetland"];
    );
      '''
}

expandedsources = ['roads', 'roads-labels']


class GoogleProjection:
    def __init__(self, levels=18):
        self.Bc = []
        self.Cc = []
        self.zc = []
        self.Ac = []
        c = 256
        for d in range(0, levels):
            e = c/2
            self.Bc.append(c/360.0)
            self.Cc.append(c/(2 * math.pi))
            self.zc.append((e, e))
            self.Ac.append(c)
            c *= 2

    def fromLLtoPixel(self, ll, zoom):
        d = self.zc[zoom]
        e = round(d[0] + ll[0] * self.Bc[zoom])
        f = minmax(math.sin(math.radians(ll[1])), -0.9999, 0.9999)
        g = round(d[1] + 0.5*math.log((1+f)/(1-f))*-self.Cc[zoom])
        return (e, g)

    def fromPixelToLL(self, px, zoom):
        e = self.zc[zoom]
        f = (px[0] - e[0])/self.Bc[zoom]
        g = (px[1] - e[1])/-self.Cc[zoom]
        h = math.degrees(2 * math.atan(math.exp(g)) - 0.5 * math.pi)
        return (f, h)


useData = True
render_size = 256
maxZoom = 22

merc = Projection('+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +no_defs +over')
tileproj = GoogleProjection(maxZoom+1)


def tileno2bbox(x, y, z):
    # Calculate pixel positions of bottom-left & top-right
    p0 = (x * 256, (y + 1) * 256)
    p1 = ((x + 1) * 256, y * 256)

    # Convert to LatLong (EPSG:4326)
    l0 = tileproj.fromPixelToLL(p0, z)
    l1 = tileproj.fromPixelToLL(p1, z)

    # Convert to map projection (e.g. mercator co-ords EPSG:900913)
    c0 = merc.forward(Coord(l0[0], l0[1]))
    c1 = merc.forward(Coord(l1[0], l1[1]))

    # Bounding box for the tile
    return Box2d(c0.x, c0.y, c1.x, c1.y)


def tileno2latlong(x, y, z):
    # Calculate pixel positions of bottom-left & top-right
    p0 = (x * 256, (y + 1) * 256)
    p1 = ((x + 1) * 256, y * 256)

    # Convert to LatLong (EPSG:4326)
    l0 = tileproj.fromPixelToLL(p0, z)
    l1 = tileproj.fromPixelToLL(p1, z)

    # Convert to map projection (e.g. mercator co-ords EPSG:900913)
    c0 = Coord(l0[0], l0[1])
    c1 = Coord(l1[0], l1[1])

    # Bounding box for the tile
    return Box2d(c0.x, c0.y, c1.x, c1.y)


class DBFetcherQueue(object):
    def __init__(self):
        self._lock = Lock()
        self._queue = []

    def get(self, x, y, z, source):
        job = DBJob(x, y, z, source)
        self._lock.acquire()
        if job not in self._queue:
            self._queue += [job]
            self._lock.release()

            job.generate()

            self._lock.acquire()
            self._queue.remove(job)
            self._lock.release()

            return job.sdb
        else:
            job = next(j for j in self._queue if j == job)
            self._lock.release()
            job.wait()
            return job.sdb

    def genTop(self):
        self.queue.popitem(0).generate()


class DBJob(object):
    file_lock = Lock()
    dir_lock = Lock()
    overpass_lock = Lock()
    db_locks = {}

    def __init__(self, x, y, z, source):
        self.source = source
        self.x = x
        self.y = y
        self.z = z
        self.sdb = dbFormat.format(z, x, y)
        self.sosm = osmFormat.format(z, x, y, self.source)
        self.doneEvent = Event()

    def __eq__(self, other):
        if other.source != self.source:
            return False
        if self.x != other.x:
            return False
        if self.y != other.y:
            return False
        if self.z != other.z:
            return False
        return True

    def wait(self):
        self.doneEvent.wait()

    def generate(self):
        DBJob.file_lock.acquire()
        if not exists(self.sosm) or not exists(self.sdb):
            if self.sdb not in DBJob.db_locks:
                DBJob.db_locks[self.sdb] = Lock()
            DBJob.file_lock.release()

            print 'fetching {}...'.format(self.sosm)
            boxlatlong = tileno2latlong(self.x, self.y, self.z)
            if self.source in expandedsources:
                expw = boxlatlong.width()/50.0
                exph = boxlatlong.height()/50.0
            else:
                expw = 0.0
                exph = 0.0

            boxlatlong = Box2d(boxlatlong.minx-expw, boxlatlong.miny-exph, boxlatlong.maxx+expw, boxlatlong.maxy+exph)
            response = None
            with DBJob.overpass_lock:
                retry = 0
                while retry < OSM_MAX_RETRIES:
                    try:
                        import overpass
                        api = overpass.API('http://overpass-api.de/api/interpreter', timeout=None)
                        r = api._get_from_overpass('''
                        [out:json][bbox:{0},{1},{2},{3}];
                        {4}
                        out meta;
                        >;
                        out skel qt;
                        '''.format(boxlatlong.miny, boxlatlong.minx, boxlatlong.maxy, boxlatlong.maxx, datasources[self.source]))
                        r.encoding = 'UTF-8'
                        response = r.text
                        break
                    except overpass.MultipleRequestsError:
                        time.sleep(3*retry)
                        retry += 1

            if response is not None:
                dirpath = dirname(self.sosm)

                DBJob.dir_lock.acquire()
                if not os.path.exists(dirpath):
                    os.makedirs(dirpath)
                DBJob.dir_lock.release()

                with open(self.sosm, 'wb') as w:
                    w.write(response.encode('utf8', 'replace'))

                dirpath = dirname(self.sdb)
                DBJob.dir_lock.acquire()
                if not os.path.exists(dirpath):
                    os.makedirs(dirpath)
                DBJob.dir_lock.release()

                with DBJob.db_locks[self.sdb]:
                    toSpatial(self.sosm, self.sdb)

                #with open(self.sosm, 'w') as w:
                #    w.write('')
        else:
            DBJob.file_lock.release()

        self.doneEvent.set()


class TileGenQueue(object):

    def __init__(self):
        self._lock = Lock()
        self._queue = OrderedDict()

    def get(self, file):
        self._lock.acquire()
        if file not in self._queue:
            print 'adding...'
            job = TileGenJob(file)
            self._queue[file] = job
            self._lock.release()

            job.generate()
            img = job.readImage()

            self._lock.acquire()
            self._queue.pop(file)
            self._lock.release()

            return img
        else:
            job = self._queue[file]
            self._lock.release()
            return job.readImage()

    def genTop(self):
        self.queue.popitem(0).generate()


tileJobQueue = TileGenQueue()
dbJobQueue = DBFetcherQueue()


class TileGenJob(object):
    dir_lock = Lock()

    def __init__(self, img):
        self.img = img
        self.doneEvent = Event()

    def wait(self):
        self.doneEvent.wait()

    def readImage(self):
        self.wait()
        with open(self.img, 'rb') as imagefd:
            return imagefd.read()

    def generate(self):
        local = self.img
        if os.path.exists(local):
            self.doneEvent.set()
            return

        dirpath = dirname(local)

        TileGenJob.dir_lock.acquire()
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)
        TileGenJob.dir_lock.release()

        parts = os.path.normpath(self.img)
        print self.img
        print parts
        print parts.split(os.sep)
        d, z, x, y = parts.split(os.sep)
        y = os.path.splitext(y)[0]

        x = int(x)
        y = int(y)
        z = int(z)

        if useData and z >= 12:
            topz = z
            topx = x
            topy = y
            mapstring = ''
            with open(mapfile, 'r') as f:
                mapstring = f.read()
            while (topz > 12):
                topz -= 1
                topx /= 2
                topy /= 2
            for source in datasources:
                sdb = dbJobQueue.get(topx, topy, topz, source)
            mapstring = mapstring.replace(DB_REPLACE, sdb)
        else:
            mapstring = emptymapstring

        print 'loading...'

        m = Map(render_size, render_size)
        load_map_from_string(m, mapstring)
        print 'loaded...'
        print m.envelope()
        bbox = m.envelope()
        long = -105.2501
        lat = 40.0237
        import sys
        zoom = float(sys.argv[1])
        print 'tilebox...'
        bounds = tileno2bbox(x, y, z)
        print 'resize...'
        m.resize(render_size, render_size)
        print 'zoom...'
        m.zoom_to_box(bounds)
        m.buffer_size = render_size/2
        print 'render & write...'
        render_to_file(m, local, 'png')
        # im = Image(render_size, render_size)
        # render(m, im)
        # im.save(local, 'png')

        self.doneEvent.set()


class Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        local = join('www', self.path[1:])
        print 'Request {}...'.format(local)
        img = tileJobQueue.get(local)
        self.send_response(200)
        self.send_header('Content-type', 'image/png')
        self.end_headers()
        self.wfile.write(img)

    def do_HEAD(self):
        pass


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""


def mapSetup():
    gdal.SetCacheMax(500000000)
    global emptymapstring
    if not exists(emptydb) and not exists(emptyosm):
        response = '''
        {
          "version": 0.6,
          "generator": "Overpass API 0.7.55.4 3079d8ea",
          "osm3s": {
            "timestamp_osm_base": "2018-08-23T14:53:03Z",
            "copyright": "The data included in this document is from www.openstreetmap.org. The data is made available under ODbL."
          },
          "elements": []
        }
        '''
        with open(emptyosm, 'w') as w:
            w.write(response)

    if not exists(emptydb):
        toSpatial(emptyosm, emptydb)

    if not exists(emptymapfile):
        emptymapstring = ''
        with open(mapfile, 'r') as f:
            emptymapstring = f.read()
            emptymapstring = emptymapstring.replace(DB_REPLACE, emptydb)
    else:
        with open(emptymapfile, 'r') as f:
            f.write(emptymapstring)


def run(port=80):
    mapSetup()
    server = ThreadedHTTPServer(('', port), Handler)
    print 'Starting server, use <Ctrl-C> to stop'

    server.serve_forever()


if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
