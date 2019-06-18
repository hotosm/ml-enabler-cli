import json
from click.testing import CliRunner
from ml_enabler.cli import main_group


def test_looking_glass_aggregator():
    infile = 'ml_enabler/tests/fixtures/looking_glass_output.json'
    expected_results = json.load(open('ml_enabler/tests/fixtures/looking_glass_aggregator_output.json'))
    outfile = '/tmp/aggregator.json'
    errfile = '/tmp/err.json'

    runner = CliRunner()
    result = runner.invoke(main_group,
                           ['aggregate_predictions', '--zoom', 14, '--infile', infile, '--outfile', outfile, '--errfile', errfile])
    current_results = json.load(open(outfile))
    assert(result.exit_code) == 0
    assert(expected_results == current_results)
