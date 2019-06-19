from area import area
import json
import numpy as np
import os
import subprocess
import tempfile


def get_osm(aoi):
    # convert AOI to bounding box
    pass


class OSMData(object):

    def __init__(self, aoi, overpass_url='https://lz4.overpass-api.de/api/interpreter'):
        self.aoi = aoi
        self.url = overpass_url
        self.geojson = None

    @property
    def bbox(self):
        """ Get bounding box of AOI """
        coords = np.array(self.aoi['geometry']['coordinates']).squeeze()
        lons = [c[0] for c in coords]
        lats = [c[1] for c in coords]
        return [min(lons), min(lats), max(lons), max(lats)]

    @classmethod
    def _to_geojson(cls, data):
        geojson = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [d["lon"], d["lat"]],
                        },
                    "properties": d,
                } for d in data]
        }
        return geojson

    @classmethod
    def run_command(cls, cmd):
        """ Run cmd as a system command """
        try:
            out = subprocess.check_output(cmd.split(' '), stderr=subprocess.STDOUT)
            return out
        except Exception:
            raise RuntimeError('Error running %s' % cmd)

    @classmethod
    def to_geojson(cls, osmdata):
        """ Convert OSM data to GeoJSON using osmtogeojson """
        with tempfile.TemporaryDirectory() as outdir:
            outfile = os.path.join(outdir, 'osm.osm')
            # logger.debug('Writing OSM data to temp file %s' % outfile)
            with open(outfile, 'w') as f:
                f.write(osmdata)
            geojson = json.loads(cls.run_command('osmtogeojson %s' % outfile))
            os.remove(outfile)
        return geojson

    async def building_area(self, session):
        geojson = await self.fetch(session)
        total = 0
        for f in geojson['features']:
            total += area(f['geometry'])
        return total

    async def fetch(self, session):
        """ Fetch OSM data within an AOI as GeoJSON """
        # osm bounding box: (south, west, north, east)
        if self.geojson is not None:
            return self.geojson
        q = self.build_query()
        resp = await session.get(self.url, data=q)
        if resp.status == 200:
            self.geojson = self.to_geojson(await resp.text())
            return self.geojson
        else:
            raise Exception('Error fetching OSM data from Overpass')

    def build_query(self, bbox=False, format='xml'):
        # poly
        if bbox:
            geoq = '%s, %s, %s, %s' % (self.bbox[1], self.bbox[0], self.bbox[3], self.bbox[2])
        else:
            coords = np.array(self.aoi['geometry']['coordinates']).squeeze()
            _coords = ['%s %s' % (c[1], c[0]) for c in coords]
            geoq = 'poly:"%s"' % ' '.join(_coords)

        # types = ('node["building"="yes"]', 'way["building"="yes"]', 'relation["building"="yes"]')
        types = ('way["building"]',)
        # types = ('way["building"="yes"]')
        q = '[out:%s];(%s);out geom;' % (format, ''.join(['%s(%s);' % (t, geoq) for t in types]))
        # q = '[out:xml];way["building"="yes"](%s);out geom;' % geoq
        # logger.debug(q)
        return q
