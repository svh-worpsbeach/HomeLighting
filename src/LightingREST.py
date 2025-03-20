# Assisted by watsonx Code Assistant 
from flask import Flask, request, jsonify

import logging.handlers
import json

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class LightingREST:

    fixtures = None

    def get_fixture(self, identifier):
        fixture = None

        for f in self.fixtures:
             if f.get_name() == identifier:
                fixture=f
                pass

        return fixture
    
    def __init__(self, fixtures):
        self.fixtures = fixtures
        self.app = Flask(__name__)
        # self.lights = {}  # Hypothetical lighting system state

        @self.app.route('/fixtures/count', methods=['GET'])
        def get_light_count():
            logger.debug(f"request: light count")
            if len(self.lighting.fixtures) > 0:
                logger.debug(len(self.lighting.fixtures))
                return jsonify({'count': len(self.lighting.fixtures)})
            else:
                return jsonify({'error': 'no lights defined'}), 404
        
        @self.app.route('/fixtures/names', methods=['GET'])
        def get_light_names():
            logger.debug(f"request: light names")
            names = []

            for fix in self.lighting.fixtures:
                name = fix.get_name()
                names.append(name)

            if len(names) > 0:
                logger.debug(jsonify({'names': names}))
                return jsonify({'names': names})
            else:
                return jsonify({'error': 'no fixtures defined'}), 404

        @self.app.route('/fixtures/<string:fixture_id>', methods=['GET'])
        def get_light_status(fixture_id):
            logger.debug(f"request: light defnition of {fixture_id}")
            fixture = self.get_fixture(fixture_id)

            if fixture != None:
                logger.debug(fixture)
                json_data = json.dumps(fixture, default=lambda o: o.__dict__, indent=4)
                return json_data
            else:
                return jsonify({'error': 'Fixture not found'}), 404

        #@self.app.route('/lights/<string:light_id>', methods=['PUT'])
        #def update_light_status(light_id):
        #    if light_id in self.lights:
        #        data = request.get_json()
        #        self.lights[light_id] = data
        #        return jsonify({'status': 'success'})
        #    else:
        #        return jsonify({'error': 'Light not found'}), 404

        #@self.app.route('/lights', methods=['POST'])
        #def add_light():
        #    data = request.get_json()
        #    light_id = data.get('id')
        #    if light_id not in self.lights:
        #        self.lights[light_id] = data
        #        return jsonify({'status': 'success', 'light_id': light_id}), 201
        #    else:
        #        return jsonify({'error': 'Light already exists'}), 409

        #@self.app.route('/lights', methods=['DELETE'])
        #def delete_light():
        #    light_id = request.args.get('id')
        #    if light_id in self.lights:
        #        del self.lights[light_id]
        #        return jsonify({'status': 'success'})
        #    else:
        #        return jsonify({'error': 'Light not found'}), 404

    def run(self, host='0.0.0.0', port=9999):
        logger.debug(f"starting REST server on host {host}:{port}")
        self.app.run(host=host, port=port)

if __name__ == '__main__':
    lighting_rest = LightingREST(None)
    lighting_rest.run()
