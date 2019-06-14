import json

class BaseAggregator:
    
    def __init__(self, zoom, infile, outfile, errfile):
        self.zoom = zoom
        self.source_data = json.load(infile)
        self.outfile = outfile
        self.errfile = errfile

    async def aggregate(self):
        '''
            Write out aggregations to outfile
        '''
        raise NotImplementedError('Implement aggregate method in your Prediction class')


