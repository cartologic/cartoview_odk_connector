create_view = 'CREATE OR REPLACE VIEW "%s" AS SELECT *, ST_SetSRID(ST_MakePoint("LOCATION_LNG", "LOCATION_LAT"), 4326) AS the_geom FROM "%s";'