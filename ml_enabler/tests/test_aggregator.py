from ml_enabler.aggregators.LookingGlassAggregator import LookingGlassAggregator
from ml_enabler.commands.aggregate_predictions import aggregate
import json
from click.testing import CliRunner
from ml_enabler.cli import main_group
import pytest
import aiohttp
import asyncio
import aresponses

@pytest.mark.asyncio
async def test_looking_glass_aggregator(event_loop):
    infile = 'ml_enabler/tests/fixtures/looking_glass_output.json'
    expected_results = json.load(open('ml_enabler/tests/fixtures/looking_glass_aggregator_output.json'))
    outfile = '/tmp/aggregator.json'
    errfile = '/tmp/err.json'
    overpass_response = open('ml_enabler/tests/fixtures/overpass.xml').read()
    async with aresponses.ResponsesMockServer(loop=event_loop) as arsps:

        arsps.add('overpass.maptime.in', '/api/interpreter', 'get', arsps.Response(text=overpass_response, status=200))

    # runner = CliRunner()
    # result = runner.invoke(main_group,
    #          ['aggregate_predictions', '--zoom', 14, '--infile', infile, '--outfile', outfile, '--errfile', errfile])

        aggregator = LookingGlassAggregator(14, open(infile), open(outfile, 'w'), open(errfile, 'w'))
        await aggregator.aggregate(event_loop)

        current_results = json.load(open(outfile))
    # assert(result.exit_code) == 0
        assert(expected_results == current_results)
