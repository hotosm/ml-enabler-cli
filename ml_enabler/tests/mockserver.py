# adapted from https://gist.github.com/eruvanos/f6f62edb368a20aaa880e12976620db8

import requests

from flask import jsonify
from threading import Thread


class MockServer(Thread):
    def __init__(self, port=5000):
        super().__init__()
        from flask import Flask
        self.port = port
        self.app = Flask(__name__)
        self.url = "http://localhost:%s" % self.port

        self.app.add_url_rule("/shutdown", view_func=self._shutdown_server)

    def _shutdown_server(self):
        from flask import request
        if not 'werkzeug.server.shutdown' in request.environ:
            raise RuntimeError('Not running the development server')
        request.environ['werkzeug.server.shutdown']()
        return 'Server shutting down...'

    def shutdown_server(self):
        requests.get("http://localhost:%s/shutdown" % self.port)
        self.join()

    def add_callback_response(self, url, callback, methods=('GET',)):
        self.app.add_url_rule(url, view_func=callback, methods=methods)

    def add_json_response(self, url, serializable, methods=('GET',)):
        def callback():
            return jsonify(serializable)

        self.add_callback_response(url, callback, methods=methods)

    def run(self):
        self.app.run(port=self.port)


# if __name__ == '__main__':
#     mockserver = MockServer(1234)
#     def overpass_callback():
#         overpass_response = open('ml_enabler/tests/fixtures/overpass_response.xml').read()
#         print('overpass', overpass_response)
#         return overpass_response
#     mockserver.add_callback_response('/api/interpreter', overpass_callback)
#     mockserver.run()
