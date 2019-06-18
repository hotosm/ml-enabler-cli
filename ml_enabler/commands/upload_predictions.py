import click
import json
from ml_enabler.utils.api import get_model_id, post_prediction, post_prediction_tiles

@click.command('upload_predictions', short_help='Upload predictions JSON to the ML Enabler API')
@click.option('--infile', help='Filename to read predictions JSON from', type=click.File('r'))
@click.option('--api-url', help='ML Enabler API URL', default='http://localhost:5000/')
@click.pass_context
def upload(ctx, infile, api_url):
    data = json.load(infile)
    metadata = data['metadata']
    predictions = data['predictions']
    model_name = metadata['model_name']
    model_id = get_model_id(api_url, model_name)
    bbox = metadata['bbox']
    version = metadata['version']
    zoom = metadata['zoom']
    prediction_id = post_prediction(api_url, model_id, version, zoom, bbox)
    for p in predictions:
        p['prediction_id'] = prediction_id
    post_prediction_tiles(api_url, prediction_id, predictions)
    print(f'uploaded predictions to model_id={model_id}, prediction_id={prediction_id}')


    
    
