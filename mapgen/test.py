#!/usr/bin/python

import json
import pyspatialite.dbapi2 as db
#con = db.connect(':memory:')

# Test that the spatialite extension has been loaded:
#cursor = con.execute('SELECT sqlite_version(), spatialite_version()')
#print cursor.fetchall()
import sys
from spatialconv.conv import toSpatial

toSpatial(sys.argv[1], sys.argv[2])
