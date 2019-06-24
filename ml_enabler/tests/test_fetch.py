import json
from click.testing import CliRunner
import os
import flask
from ml_enabler.cli import main_group
from ml_enabler.tests.mockserver import MockServer


def test_looking_glass_fetch():

    def get_fake_tile():
        return flask.send_file('fixtures/fake_tile.png')

    def get_looking_glass_prediction():
        text = open('ml_enabler/tests/fixtures/looking_glass_prediction.json').read()
        res = flask.Response(
            text,
            mimetype='application/json'
        )
        res.headers['Content-Length'] = len(res.get_data())
        return res

    server = MockServer(port=1234)
    server.start()
    looking_glass_metadata = json.load(open('ml_enabler/tests/fixtures/looking_glass_metadata.json'))
    server.add_callback_response('/tile', get_fake_tile)
    server.add_json_response('/v1/models/looking_glass', looking_glass_metadata)
    server.add_callback_response('/v1/models/looking_glass:predict', get_looking_glass_prediction)
    outfile = '/tmp/predict_fetch.json'
    errfile = '/tmp/err.json'
    tile_url = 'http://localhost:1234/tile'
    endpoint = 'http://localhost:1234/v1/'
    runner = CliRunner()
    result = runner.invoke(main_group,
                           [
                               'fetch_predictions',
                               '--name',
                               'looking_glass',
                               '--zoom',
                               18,
                               '--concurrency',
                               1,
                               '--bbox',
                               '15.098834,47.379869,15.105771,47.383678',
                               '--token',
                               'abc',
                               '--outfile',
                               outfile,
                               '--errfile',
                               errfile,
                               '--endpoint',
                               endpoint,
                               '--tile-url',
                               tile_url
                            ])
    current_results = json.load(open(outfile))
    expected_results = json.load(open('ml_enabler/tests/fixtures/looking_glass_fetch_expected.json'))
    server.shutdown_server()
    os.remove(outfile)
    os.remove(errfile)
    assert(result.exit_code == 0)
    # we don't test that the entire JSONs are equivalent because of an unknown amount of request errors from the flask mock server
    assert(current_results['metadata'] == expected_results['metadata'])
    assert(current_results['predictions'][0]['predictions']['ml_prediction'] == expected_results['predictions'][0]['predictions']['ml_prediction'])


def test_building_api_fetch():
    server = MockServer(port=1234)
    server.start()
    building_api_response = json.load(open('ml_enabler/tests/fixtures/building_api_response.json'))
    server.add_json_response('/building_api', building_api_response)
    outfile = '/tmp/predict_fetch.json'
    errfile = '/tmp/err.json'
    endpoint = 'http://localhost:1234/building_api'
    runner = CliRunner()
    result = runner.invoke(main_group,
                           [
                               'fetch_predictions',
                               '--name',
                               'building_api',
                               '--zoom',
                               16,
                               '--concurrency',
                               1,
                               '--bbox',
                               '-77.14,38.82,-76.92,38.95',
                               '--token',
                               'abc',
                               '--outfile',
                               outfile,
                               '--errfile',
                               errfile,
                               '--endpoint',
                               endpoint
                            ])
    current_results = json.load(open(outfile))
    expected_results = json.load(open('ml_enabler/tests/fixtures/building_fetch_expected_output.json'))
    expected_results['predictions'] = sorted(expected_results['predictions'], key=lambda p: p['quadkey'])
    current_results['predictions'] = sorted(current_results['predictions'], key=lambda p: p['quadkey'])
    server.shutdown_server()
    assert(result.exit_code == 0)
    assert(current_results == expected_results)
