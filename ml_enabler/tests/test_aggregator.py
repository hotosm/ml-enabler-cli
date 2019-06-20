import json
from click.testing import CliRunner
import os
from ml_enabler.cli import main_group
from ml_enabler.tests.mockserver import MockServer


def test_looking_glass_aggregator():

    def overpass_callback():
        overpass_response = open('ml_enabler/tests/fixtures/overpass_response.xml').read()
        return overpass_response

    server = MockServer(port=1234)
    server.start()
    server.add_callback_response('/api/interpreter', overpass_callback)
    infile = 'ml_enabler/tests/fixtures/looking_glass_output.json'
    expected_results = json.load(open('ml_enabler/tests/fixtures/looking_glass_aggregator_output.json'))
    outfile = '/tmp/aggregator.json'
    errfile = '/tmp/err.json'

    runner = CliRunner()
    result = runner.invoke(main_group,
                           ['aggregate_predictions', '--name', 'looking_glass',  '--zoom', 14, '--infile', infile, '--outfile', outfile, '--errfile', errfile, '--overpass-url', 'http://localhost:1234/api/interpreter'])
    current_results = json.load(open(outfile))
    expected_results['predictions'] = sorted(expected_results['predictions'], key=lambda p: p['quadkey'])
    current_results['predictions'] = sorted(current_results['predictions'], key=lambda p: p['quadkey'])
    assert(result.exit_code) == 0
    assert(expected_results == current_results)
    server.shutdown_server()
    os.remove('/tmp/aggregator.json')



def test_building_aggregator():

    def overpass_callback():
        overpass_response = open('ml_enabler/tests/fixtures/overpass_response.xml').read()
        return overpass_response

    server = MockServer(port=1234)
    server.start()
    server.add_callback_response('/api/interpreter', overpass_callback)
    infile = 'ml_enabler/tests/fixtures/building_api_output.json'
    expected_results = json.load(open('ml_enabler/tests/fixtures/building_api_aggregator_output.json'))
    outfile = '/tmp/aggregator.json'
    errfile = '/tmp/err.json'

    runner = CliRunner()
    result = runner.invoke(main_group,
                           ['aggregate_predictions', '--name', 'building_api',  '--zoom', 14, '--infile', infile, '--outfile', outfile, '--errfile', errfile, '--overpass-url', 'http://localhost:1234/api/interpreter'])
    current_results = json.load(open(outfile))
    expected_results['predictions'] = sorted(expected_results['predictions'], key=lambda p: p['quadkey'])
    current_results['predictions'] = sorted(current_results['predictions'], key=lambda p: p['quadkey'])
    server.shutdown_server()
    assert(result.exit_code) == 0
    assert(expected_results == current_results)
    os.remove('/tmp/aggregator.json')
    