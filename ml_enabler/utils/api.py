import requests


def get_model_id(api_url, model_name):
    url = f'{api_url}/model/all'
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception('Failed to fetch model id for model name')
    data = response.json()
    for model in data:
        if model['name'] == model_name:
            return model['modelId']
    raise Exception('Model with that name does not exist')


def post_prediction(api_url, model_id, version, zoom, bbox):
    url = f'{api_url}/model/{model_id}/prediction'
    data = {
        'version': f'{version}.0.0',
        'modelId': model_id,
        'bbox': bbox.split(','),
        'tileZoom': zoom
    }
    print(data)
    response = requests.post(url, json=data)
    if response.status_code != 200:
        raise Exception('could not POST Prediction')
    response_data = response.json()
    return response_data['prediction_id']


def post_prediction_tiles(api_url, prediction_id, predictions):
    url = f'{api_url}/model/prediction/{prediction_id}/tiles'
    data = {
        'predictionId': prediction_id,
        'predictions': predictions
    }
    response = requests.post(url, json=data)
    if response.status_code != 200:
        raise Exception('Error posting tiles for prediction')
    return True
