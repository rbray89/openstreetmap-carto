#FROM docker.io/project31/aarch64-alpine-qemu:3.5
#RUN [ "cross-build-start" ]

ARG BUILD_FROM
FROM $BUILD_FROM

RUN apk add --no-cache \
    python2=2.7.15-r1 \
    python2-dev=2.7.15-r1 \
    sphinx=2.2.11-r1 \
    icu
RUN \
  apk add --no-cache \
  --repository http://dl-cdn.alpinelinux.org/alpine/edge/testing \
  boost\
  boost-python \
  proj4 \
  tiff \
  cairo \
  icu \
  libpng \
  libwebp \
  sqlite \
  freetype \
  libxml2 \
  gdal \
  py-gdal \
  harfbuzz \
  py-setuptools \
  font-noto \
  boost-program_options

# Setup base
RUN \
  apk add --no-cache --virtual .build-dependencies \
  --repository http://dl-cdn.alpinelinux.org/alpine/edge/testing \
    g++ \
    gcc \
    zlib-dev \
    curl \
    git \
    make \
    py2-pip \
    openssh \
    cmake \
    automake \
    autoconf \
    libtool \
    linux-headers \
    boost-dev \
    cairo-dev \
    freetype-dev \
    gdal-dev \
    harfbuzz-dev \
    icu-dev \
    libpng-dev \
    libwebp-dev \
    libxml2-dev \
    proj4-dev \
    python3 \
    sqlite-dev \
    tiff-dev \
    zlib-dev \
	postgresql-dev \
    proj4-dev \
    swig \
    boost-python
RUN mkdir -p ~/.ssh/ \
  && ssh-keyscan github.com >> ~/.ssh/known_hosts
RUN wget -O tmp/config.guess 'https://git.savannah.gnu.org/cgit/config.git/plain/config.guess?id=7d3d27baf8107b630586c962c057e22149653deb' \
  && wget -O tmp/config.sub 'https://git.savannah.gnu.org/cgit/config.git/plain/config.sub?id=7d3d27baf8107b630586c962c057e22149653deb'

RUN pip install --no-cache-dir --upgrade \
    setuptools==40.0.0

RUN wget http://download.osgeo.org/geos/geos-3.6.2.tar.bz2 \
  && tar -xvf geos-3.6.2.tar.bz2 \
  && cp tmp/config.guess geos-3.6.2 \
  && cp tmp/config.sub geos-3.6.2 \
  && cd geos-3.6.2 \
  && ./configure \
    --build=$CBUILD \
    --host=$CHOST \
    --prefix=/usr \
    --sysconfdir=/etc \
    --mandir=/usr/share/man \
    --localstatedir=/var \
    --enable-python \
    && make \
    && make install \
  && cd .. \
  && rm -rf geos-3.6.2

RUN wget http://www.gaia-gis.it/gaia-sins/libspatialite-4.3.0a.tar.gz \
  && tar -xvf libspatialite-4.3.0a.tar.gz \
  && cp tmp/config.guess libspatialite-4.3.0a \
  && cp tmp/config.sub libspatialite-4.3.0a \
  && cd libspatialite-4.3.0a \
  && ./configure \
    --prefix=/usr \
    --build=$CBUILD \
    --host=$CHOST \
    --enable-freexl=no \
    && make \
    && make install \
  && cd .. \
  && rm -rf libspatialite-4.3.0a

RUN git clone https://github.com/lokkju/pyspatialite.git \
  && cd pyspatialite \
    && python setup.py install
RUN CFLAGS="-I/usr/include -I/usr/local/include" pip install --no-cache-dir  \
    overpass==0.6.0

RUN git clone https://github.com/mapnik/mapnik mapnik --depth 10 \
  && cd mapnik && git submodule update --init \
  && ./configure && make && make install \
  && cd .. \
  && rm -rf mapnik

RUN git clone https://github.com/mapnik/python-mapnik.git \
  && cd python-mapnik \
    && export BOOST_PYTHON_LIB=boost_python \
    && python setup.py install \
  && cd .. \
  && rm -rf python-mapnik

RUN apk del --purge .build-dependencies

# Copy data for add-on
RUN mkdir /mapgen
COPY spatialconv /mapgen/spatialconv
COPY server.py /mapgen/server.py
COPY get-shapefiles.py /mapgen/get-shapefiles.py
COPY mapnik.xml /mapgen/mapnik.xml
COPY run.sh /run.sh
RUN chmod +x /mapgen/server.py
RUN chmod +x /mapgen/get-shapefiles.py
RUN chmod +x /run.sh
RUN ln -s /share/mapgen/www /mapgen/www
RUN ln -s /share/mapgen/data /mapgen/data
RUN ln -s /share/mapgen/symbols /mapgen/symbols

CMD [ "/run.sh" ]
#RUN [ "cross-build-end" ]
