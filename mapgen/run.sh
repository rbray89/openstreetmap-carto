#!/bin/sh

# Downloading needed shapefiles
python get-shapefiles.py -n

python /server.py 8000
