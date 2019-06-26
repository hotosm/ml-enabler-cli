import json


class BaseAggregator:
    def __init__(self, zoom, overpass_url, infile, outfile):
        data = json.load(infile)
        self.zoom = zoom
        current_zoom = data['metadata']['zoom']
        if zoom > current_zoom:
            raise ValueError('Output zoom cannot be higher than current zoom level.')
        self.overpass_url = overpass_url
        self.source_data = data['predictions']
        self.source_metadata = data['metadata']
        self.outfile = outfile

    async def aggregate(self):
        '''
            Write out aggregations to outfile
        '''
        raise NotImplementedError('Implement aggregate method in your Prediction class')
