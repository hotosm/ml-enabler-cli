import json
from click.testing import CliRunner
import httpretty
from ml_enabler.cli import main_group


@httpretty.activate
def test_looking_glass_aggregator():
    overpass_fake_data = open('ml_enabler/tests/fixtures/overpass_response.xml').read()
    httpretty.register_uri(
        httpretty.GET,
        'http://overpass.fake/api/interpreter',
        body=overpass_fake_data
    )
    infile = 'ml_enabler/tests/fixtures/looking_glass_output.json'
    expected_results = json.load(open('ml_enabler/tests/fixtures/looking_glass_aggregator_output.json'))
    outfile = '/tmp/aggregator.json'
    errfile = '/tmp/err.json'
    runner = CliRunner()
    result = runner.invoke(main_group,
                           ['aggregate_predictions', '--name', 'looking_glass', '--zoom', 14, '--overpass-url', 'http://overpass.fake/api-interpreter', '--infile', infile, '--outfile', outfile, '--errfile', errfile])
    current_results = json.load(open(outfile))
    assert(result.exit_code) == 0
    assert(expected_results == current_results)
