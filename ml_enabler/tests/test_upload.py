import json
from click.testing import CliRunner
from ml_enabler.cli import main_group
from ml_enabler.tests.mockserver import MockServer
import flask


def test_upload():

    def get_model_all_response():
        data = [
            {
                "modelId": 1,
                "created": "2019-05-31T10:55:27.636457",
                "name": "looking_glass",
                "source": "developmentseed",
                "dockerhubUrl": "dockerhubUrl"
            }
        ]

        res = flask.Response(
              json.dumps(data),
              mimetype='application/json'
        )
        return res

    def add_prediction_response():
        data = {'prediction_id': 1}
        res = flask.Response(
            json.dumps(data),
            mimetype='application/json'
        )
        return res

    def post_prediction_response():
        res = flask.Response()
        return res

    server = MockServer(port=1234)
    server.start()
    server.add_callback_response('/v1/model/all', get_model_all_response)
    server.add_callback_response('/v1/model/1/prediction', add_prediction_response)
    server.add_callback_response('/v1/model/prediction/1/tiles', post_prediction_response)

    infile = 'ml_enabler/tests/fixtures/looking_glass_aggregator_output.json'

    runner = CliRunner()
    result = runner.invoke(main_group,
                           ['upload_predictions', '--infile', infile, '--api-url', 'http://localhost:1234/v1'])

    server.shutdown_server()
    assert(result.exit_code == 0)
