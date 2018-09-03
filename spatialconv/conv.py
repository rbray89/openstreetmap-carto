#!/usr/bin/python

import json
import pyspatialite.dbapi2 as db
from os.path import exists
from collections import OrderedDict
#con = db.connect(':memory:')

# Test that the spatialite extension has been loaded:
#cursor = con.execute('SELECT sqlite_version(), spatialite_version()')
#print cursor.fetchall()

COLUMNS = ['name', 'ref', 'ele', 'place', 'natural', 'water', 'landuse',
            'disused', 'service', 'access', 'tourism', 'leisure', 'historic', 'man_made',
            'military', 'religion', 'building', 'amenity', 'shop', 'barrier',
            'waterway', 'railway', 'aerialway', 'aeroway', 'highway', 'bridge', 'tunnel',
            'lock', 'layer', 'covered', 'surface', 'junction', 'route', 'oneway',
            'seasonal', 'intermittent', 'operator',
            'wetland', 'location',
            'admin_level', 'boundary',
            'usage', 'highspeed',
            'power', 'leaf_type', 'public_transport', 'indoor', 'entrance',
            'tracktype', 'horse', 'bicycle', 'foot', 'construction']

Z_ORDER = {
    'railway': {
        'rail': 440,
        'INT-preserved-ssy': 430,
        'INT-spur-siding-yard': 430,
        'subway': 420,
        'narrow_gauge': 420,
        'light_rail': 420,
        'preserved': 420,
        'funicular': 420,
        'monorail': 420,
        'miniature': 420,
        'turntable': 420,
        'tram': 410,
        'tram-service': 405,
        'disused': 400,
        'construction': 400,
        'platform': 90
    },
    'highway': {
        'motorway': 380,
        'trunk': 370,
        'primary': 360,
        'secondary': 350,
        'tertiary': 340,
        'residential': 330,
        'unclassified': 330,
        'road': 330,
        'living_street': 320,
        'pedestrian': 310,
        'raceway': 300,
        'motorway_link': 240,
        'trunk_link': 230,
        'primary_link': 220,
        'secondary_link': 210,
        'tertiary_link': 200,
        'service': 150,
        'track': 110,
        'path': 100,
        'footway': 100,
        'bridleway': 100,
        'cycleway': 100,
        'steps': 100,
        'platform': 90,
        'construction': 10
    },
    'aeroway': {
        'runway': 60,
        'taxiway': 50
    }
}

LAYER_Z_OFFSET = 500


def _fetchDB(dbfile):
    dbCreated = exists(dbfile)

    conn = db.connect(dbfile)

    # creating a Cursor
    cur = conn.cursor()

    # testing library versions
    rs = cur.execute('SELECT sqlite_version(), spatialite_version()')
    for row in rs:
        msg = "> SQLite v%s Spatialite v%s" % (row[0], row[1])
        print msg

    if not dbCreated:
        print 'initializing...'
        # initializing Spatial MetaData
        # using v.2.4.0 this will automatically create
        # GEOMETRY_COLUMNS and SPATIAL_REF_SYS
        sql = 'SELECT InitSpatialMetadata(1)'
        cur.execute(sql)

        print 'creating point table...'
        # creating a POINT table
        sql = 'CREATE TABLE IF NOT EXISTS points ('
        sql += 'id INTEGER NOT NULL PRIMARY KEY,'
        sql += ','.join(['{} TEXT'.format(c) for c in COLUMNS])
        sql += ',tc_id INTEGER,'
        sql += 'z_order INTEGER,'
        sql += 'FOREIGN KEY(tc_id) REFERENCES lines(id)'
        sql += ')'
        cur.execute(sql)

        print 'creating point geometry...'
        # creating a POINT Geometry column
        sql = "SELECT AddGeometryColumn('points', "
        sql += "'way', 4326, 'POINT', 'XY')"
        cur.execute(sql)
        sql = "SELECT CreateSpatialIndex('points','way')"
        cur.execute(sql)

        print 'creating line table...'
        # creating a LINESTRING table
        sql = 'CREATE TABLE IF NOT EXISTS lines ('
        sql += 'id INTEGER NOT NULL PRIMARY KEY,'
        sql += ','.join(['{} TEXT'.format(c) for c in COLUMNS])
        sql += ',z_order INTEGER'
        sql += ')'
        cur.execute(sql)
        print 'creating line geometry...'
        # creating a LINESTRING Geometry column
        sql = "SELECT AddGeometryColumn('lines', "
        sql += "'way', 4326, 'LINESTRING', 'XY')"
        cur.execute(sql)
        sql = "SELECT CreateSpatialIndex('lines','way')"
        cur.execute(sql)

        print 'creating relations table...'
        # creating a RELATIONS table
        sql = 'CREATE TABLE relations ('
        sql += 'id INTEGER NOT NULL PRIMARY KEY,'
        sql += ','.join(['{} TEXT'.format(c) for c in COLUMNS])
        sql += ',z_order INTEGER'
        sql += ',type TEXT)'
        cur.execute(sql)

        print 'creating polygon table...'
        # creating a POLYGON table
        sql = 'CREATE TABLE IF NOT EXISTS polygons ('
        sql += 'id INTEGER NOT NULL PRIMARY KEY,'
        sql += 'osm_way_id INTEGER UNIQUE,'
        sql += 'osm_relation_id INTEGER UNIQUE,'
        sql += ','.join(['{} TEXT'.format(c) for c in COLUMNS])
        sql += ',z_order INTEGER'
        sql += ',way_area DOUBLE PRECISION,'
        sql += 'FOREIGN KEY(osm_way_id) REFERENCES lines(id),'
        sql += 'FOREIGN KEY(osm_relation_id) REFERENCES relations(id))'
        cur.execute(sql)
        print 'creating polygon geometry...'
        # creating a POLYGON Geometry column
        sql = "SELECT AddGeometryColumn('polygons', "
        sql += "'way', 4326, 'MULTIPOLYGON', 'XY')"
        cur.execute(sql)
        sql = "SELECT CreateSpatialIndex('polygons','way')"
        cur.execute(sql)

        # creating a RELATIONS join table
        sql = 'CREATE TABLE IF NOT EXISTS relations_join ('
        sql += 'id INTEGER NOT NULL,'
        sql += 'member_node_id INTEGER,'
        sql += 'member_way_id INTEGER,'
        sql += 'member_relation_id INTEGER,'
        sql += 'role TEXT,'
        sql += 'PRIMARY KEY (id, member_node_id, member_way_id, member_relation_id),'
        sql += 'FOREIGN KEY(id) REFERENCES relations(id),'
        sql += 'FOREIGN KEY(member_node_id) REFERENCES points(id),'
        sql += 'FOREIGN KEY(member_way_id) REFERENCES lines(id),'
        sql += 'FOREIGN KEY(member_relation_id) REFERENCES relations(id))'
        cur.execute(sql)

        sql = '''
        CREATE TABLE IF NOT EXISTS  ordertable
        (feature TEXT PRIMARY KEY, prio INTEGER);
        INSERT INTO ordertable (feature, prio)
        VALUES
      ('railway_rail', 440),
      ('railway_INT-preserved-ssy', 430),
      ('railway_INT-spur-siding-yard', 430),
      ('railway_subway', 420),
      ('railway_narrow_gauge', 420),
      ('railway_light_rail', 420),
      ('railway_preserved', 420),
      ('railway_funicular', 420),
      ('railway_monorail', 420),
      ('railway_miniature', 420),
      ('railway_turntable', 420),
      ('railway_tram', 410),
      ('railway_tram-service', 405),
      ('railway_disused', 400),
      ('railway_construction', 400),
      ('highway_motorway', 380),
      ('highway_trunk', 370),
      ('highway_primary', 360),
      ('highway_secondary', 350),
      ('highway_tertiary', 340),
      ('highway_residential', 330),
      ('highway_unclassified', 330),
      ('highway_road', 330),
      ('highway_living_street', 320),
      ('highway_pedestrian', 310),
      ('highway_raceway', 300),
      ('highway_motorway_link', 240),
      ('highway_trunk_link', 230),
      ('highway_primary_link', 220),
      ('highway_secondary_link', 210),
      ('highway_tertiary_link', 200),
      ('highway_service', 150),
      ('highway_track', 110),
      ('highway_path', 100),
      ('highway_footway', 100),
      ('highway_bridleway', 100),
      ('highway_cycleway', 100),
      ('highway_steps', 100),
      ('highway_platform', 90),
      ('railway_platform', 90),
      ('aeroway_runway', 60),
      ('aeroway_taxiway', 50),
      ('highway_construction', 10);
      '''
        cur.executescript(sql)

    return conn, cur


def toSpatial(source, dest):
    osmjson = None
    with open(source, 'r') as fd:
        osmjson = json.load(fd)
    elements = osmjson['elements']

    conn, cur = _fetchDB(dest)

    rel_dict = {}
    for rel in (r for r in elements if r['type'] == 'relation'):
        id = rel['id']
        if id not in rel_dict:
            rel_dict[id] = rel
        elif 'tags' not in rel_dict[id] and 'tags' in rel:
            rel_dict[id] = rel

    for id, rel in rel_dict.iteritems():
        cols = OrderedDict()
        attrs = COLUMNS + ['type']
        if 'tags' in rel:
            tags = rel['tags']
            for a in [a for a in tags if a in attrs]:
                cols[a] = "'" + tags[a].replace("'", "''") + "'"
            z_order = 0
            for z in Z_ORDER:
                if z in tags:
                    try:
                        z_order = Z_ORDER[z][tags[z]]
                    except:
                        pass
                    break
            if 'layer' in tags:
                try:
                    z_order += int(tags['layer'])*LAYER_Z_OFFSET
                except:
                    pass
            cols['z_order'] = str(z_order)
        sql = "INSERT OR IGNORE INTO relations (id"
        if len(cols) > 0:
            sql += ", {}) ".format(','.join(cols.iterkeys()))
            sql += u"VALUES ({}, {})".format(id, ','.join(cols.itervalues()))
        else:
            sql += ") "
            sql += u"VALUES ({})".format(id)
        cur.execute(sql)
        for elem in rel['members']:
            type = elem['type']
            sql = "INSERT OR IGNORE INTO relations_join (id, member_{}_id, role) ".format(type)
            sql += u"VALUES ({}, {}, '{}')".format(id, elem['ref'], elem['role'])
            cur.execute(sql)
    conn.commit()


    # inserting some POINTs
    # please note well: SQLite is ACID and Transactional
    # so (to get best performance) the whole insert cycle
    # will be handled as a single TRANSACTION
    node_dict = {}
    for node in (n for n in elements if n['type'] == 'node'):
        id = node['id']
        if id not in node_dict:
            node_dict[id] = node
        elif 'tags' not in node_dict[id] and 'tags' in node:
            node_dict[id] = node

    for id, node in node_dict.iteritems():
        cols = OrderedDict()
        attrs = COLUMNS
        if 'tags' in node:
            tags = node['tags']
            for a in [a for a in tags if a in attrs]:
                cols[a] = "'" + tags[a].replace("'", "''") + "'"
            z_order = 0
            for z in Z_ORDER:
                if z in tags:
                    try:
                        z_order = Z_ORDER[z][tags[z]]
                    except:
                        pass
                    break
            if 'layer' in tags:
                try:
                    z_order += int(tags['layer'])*LAYER_Z_OFFSET
                except:
                    pass
            cols['z_order'] = str(z_order)
        else:
            continue

        geom = "SetSrid(MakePoint({:.7f}, {:.7f}),4326)".format(node['lon'], node['lat'])
        sql = "INSERT OR IGNORE INTO points (id, way"
        if len(cols) > 0:
            sql += ", {}) ".format(','.join(cols.iterkeys()))
            sql += u"VALUES ({}, {}, {})".format(id, geom, ','.join(cols.itervalues()))
        else:
            sql += ") "
            sql += u"VALUES ({}, {})".format(id, geom)
        cur.execute(sql)
    conn.commit()

    # checking POINTs
    sql = "SELECT DISTINCT Count(*), ST_GeometryType(way), "
    sql += "ST_Srid(way) FROM points"
    rs = cur.execute(sql)
    for row in rs:
        if len(row) == 3:
            msg = "> Inserted %d entities of type " % (row[0])
            msg += "{} SRID={}".format(row[1], row[2])
            print msg

    # inserting some LINESTRINGs
    way_dict = {}
    for way in (w for w in elements if w['type'] == 'way'):
        id = way['id']
        if id not in way_dict:
            way_dict[id] = way
        elif 'tags' not in way_dict[id] and 'tags' in way:
            way_dict[id] = way

    for id, way in way_dict.iteritems():
        cols = OrderedDict()
        attrs = COLUMNS
        if 'tags' in way:
            tags = way['tags']
            for a in [a for a in tags if a in attrs]:
                cols[a] = "'" + tags[a].replace("'", "''") + "'"
            z_order = 0
            for z in Z_ORDER:
                if z in tags:
                    try:
                        z_order = Z_ORDER[z][tags[z]]
                    except:
                        pass
                    break
            if 'layer' in tags:
                try:
                    z_order += int(tags['layer'])*LAYER_Z_OFFSET
                except:
                    pass
            cols['z_order'] = str(z_order)

        geom = "GeomFromText('LINESTRING("
        points = []
        for pid in way['nodes']:
            g = node_dict[pid]
            points += ['{:.7f} {:.7f}'.format(g['lon'], g['lat'])]
        geom += ', '.join(points)
        geom += ")', 4326)"
        sql = "INSERT OR IGNORE INTO lines (id, way"
        if len(cols) > 0:
            sql += ", {}) ".format(','.join(cols.iterkeys()))
            sql += u"VALUES ({}, {}, {})".format(id, geom, ','.join(cols.itervalues()))
        else:
            sql += ") "
            sql += u"VALUES ({}, {})".format(id, geom)

        cur.execute(sql)
    conn.commit()

    # checking LINESTRINGs
    sql = "SELECT DISTINCT Count(*), ST_GeometryType(way), "
    sql += "ST_Srid(way) FROM lines"
    rs = cur.execute(sql)
    for row in rs:
        if len(row) == 3:
            msg = "> Inserted %d entities of type " % (row[0])
            msg += "{} SRID={}".format(row[1], row[2])
            print msg

    sql = '''
    UPDATE points
    SET tc_id = (SELECT id
                      FROM lines
                      WHERE PtDistWithin(points.way, way, 0.1)
                      AND (points.highway = 'turning_circle' OR points.highway = 'turning_loop'))
    where EXISTS (SELECT id
                      FROM lines
                      WHERE PtDistWithin(points.way, way, 0.1)
                      AND (points.highway = 'turning_circle' OR points.highway = 'turning_loop'))
    '''
    cur.execute(sql)
    conn.commit()

    # convert relations to polygons...
    sql = '''INSERT OR IGNORE INTO polygons (osm_relation_id, {}, way_area, way)
                select
                osm_relation_id,
                {},
                Area(geom) way_area,
                geom way
                from (SELECT
                relations_join.id as osm_relation_id,
                {},
                CastToMultiPolygon(Polygonize(way)) as geom
                from relations_join, lines, relations
                where lines.id = relations_join.member_way_id
                and relations.id = relations_join.id
                and relations.type in ('polygon','multipolygon') group by relations_join.id)
                '''
    sql = sql.format(','.join(COLUMNS), ','.join(["{0}".format(c) for c in COLUMNS]), ','.join(["relations.{0} as '{0}'".format(c) for c in COLUMNS]))
    cur.execute(sql)
    conn.commit()


    # add closed lines to polygons...
    sql = '''BEGIN TRANSACTION;
        INSERT OR IGNORE INTO polygons (osm_way_id, {0}, way_area, way)
            select
            osm_way_id,
            {1},
            Area(geom) way_area,
            geom way
            from (SELECT
                id as osm_way_id,
                {1},
                CastToMultiPolygon(BuildArea(way)) as geom
                from lines where IsClosed(way));
        COMMIT;'''
    sql = sql.format(','.join(COLUMNS), ','.join(["{0}".format(c) for c in COLUMNS]))
        # DELETE FROM lines WHERE IsClosed(geom);
    cur.executescript(sql)
    conn.commit()

    # select relations_join.id, ST_UNION(geom), role from relations_join, lines where lines.id = relations_join.way_id group by relations_join.id
    #sql = 'INSERT INTO polygons (id, name, geom) select id id, name name, BuildArea(ST_Union(GEOM)) geom from lines GROUP BY IsClosed(geom);'
    #cur.execute(sql)
    #conn.commit()
    #SELECT
    #FROM GEOMTABLE GROUP BY ATTRCOLUMN

    #sql = '''UPDATE polygons '''
    #cur.execute(sql)
    #conn.commit()

    # checking POLYGONs
    sql = "SELECT DISTINCT Count(*), ST_GeometryType(way), "
    sql += "ST_Srid(way) FROM polygons"
    rs = cur.execute(sql)
    for row in rs:
        if len(row) == 3:
            msg = "> Inserted %d entities of type " % (row[0])
            msg += "{} SRID={}".format(row[1], row[2])
            print msg
    rs.close()
    conn.close()
