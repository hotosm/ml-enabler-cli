
class BasePredictor:
    
    zoom = 18 # set zoom level for Predictor, defaults to 18

    def __init__(self, endpoint, tile_url, token, zoom, model_opts):
        self.endpoint = endpoint
        self.tile_url = tile_url
        self.token = token
        self.zoom = zoom or self.default_zoom
        self.model_opts = model_opts

    async def predict(self, bbox, concurrency, out_file):
        '''
            Return predictions for given bbox
        '''
        raise NotImplementedError('Implement predict method in your Prediction class')

    async def predict_tile(self, tile):
        raise NotImplementedError('Implement predict_tile method in your Prediction class')

