#!/bin/sh

# Downloading needed shapefiles
cd mapgen/ && ./get-shapefiles.py -n -f

./server.py 8000
