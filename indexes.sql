-- These are optional but suggested indexes for rendering OpenStreetMap Carto
-- with a full planet database.
-- This file is generated with scripts/indexes.py

CREATE INDEX lines_admin
  ON lines USING GIST (way)
  WHERE boundary = 'administrative';
CREATE INDEX lines_roads_ref
  ON lines USING GIST (way)
  WHERE highway IS NOT NULL AND ref IS NOT NULL;
CREATE INDEX lines_admin_low
  ON lines USING GIST (way)
  WHERE boundary = 'administrative' AND admin_level IN ('0', '1', '2', '3', '4');
CREATE INDEX lines_ferry
  ON lines USING GIST (way)
  WHERE route = 'ferry';
CREATE INDEX lines_river
  ON lines USING GIST (way)
  WHERE waterway = 'river';
CREATE INDEX lines_name
  ON lines USING GIST (way)
  WHERE name IS NOT NULL;
CREATE INDEX polygons_water
  ON polygons USING GIST (way)
  WHERE waterway IN ('dock', 'riverbank', 'canal')
    OR landuse IN ('reservoir', 'basin')
    OR "natural" IN ('water', 'glacier');
CREATE INDEX polygons_nobuilding
  ON polygons USING GIST (way)
  WHERE building IS NULL;
CREATE INDEX polygons_name
  ON polygons USING GIST (way)
  WHERE name IS NOT NULL;
CREATE INDEX polygons_way_area_z10
  ON polygons USING GIST (way)
  WHERE way_area > 23300;
CREATE INDEX polygons_military
  ON polygons USING GIST (way)
  WHERE landuse = 'military';
CREATE INDEX polygons_way_area_z6
  ON polygons USING GIST (way)
  WHERE way_area > 5980000;
CREATE INDEX points_place
  ON points USING GIST (way)
  WHERE place IS NOT NULL AND name IS NOT NULL;
