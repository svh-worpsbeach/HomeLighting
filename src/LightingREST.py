# Assisted by watsonx Code Assistant 
from flask import Flask, request, jsonify

import logging.handlers
import json
import time

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class LightingREST:

    fixtures = None

    def get_fixture(self, identifier):
        fixture = None

        for f in self.fixtures:
             if f.get_name() == identifier:
                return (f)

        return None

    def __init__(self, fixtures, ac):
        self.fixtures = fixtures
        self.app = Flask(__name__)
        self.ac = ac
        # self.lights = {}  # Hypothetical lighting system state

        @self.app.route('/fixtures/count', methods=['GET'])
        def get_light_count():
            logger.debug(f"request: light count")

            if len(self.fixtures) > 0:
                logger.debug(len(self.fixtures))
                return jsonify({'count': len(self.fixtures)})
            else:
                return jsonify({'error': 'no lights defined'}), 404
        
        @self.app.route('/fixtures/names', methods=['GET'])
        def get_light_names():
            logger.debug(f"request: light names")

            names = list(self.fixtures.keys())

            if len(names) > 0:
                logger.debug(jsonify({'names': names}))
                return jsonify({'names': names})
            else:
                return jsonify({'error': 'no fixtures defined'}), 404
            
        @self.app.route('/fixtures/blackout', methods=['GET'])
        def black_out_fixtures():
            logger.debug(f"request: blank")

            if self.ac.blackout_all_fixtures():
                return jsonify({'status': 'success'}), 201
            else:
                return jsonify({'error': 'blanking did not work'}), 404

        @self.app.route('/fixtures/<string:fixture_id>', methods=['GET'])
        def get_light_status(fixture_id):
            logger.debug(f"request: light defnition of {fixture_id}")

            fixture = self.fixtures[fixture_id]

            if fixture != None:
                logger.debug(fixture)
                json_data = json.dumps(fixture, default=lambda o: o.__dict__, indent=4)
                return json_data
            else:
                return jsonify({'error': 'Fixture not found'}), 404

        @self.app.route('/fixture/setchannel', methods=['POST'])
        def set_fixture_channel():
            logger.debug(f"request: set channels for fixtures")

            data = request.get_json()
            fixtureList = data.get('fixtures')
            for fixtureRequest in fixtureList:

                fixtureID = fixtureRequest.get('fixtureID')

                logger.debug(f"FixtureID: {fixtureID}")

                if 'update' in fixtureRequest:
                    update = bool(fixtureRequest.get('update'))
                
                if update:
                    self.fixtures[fixtureID].clear_all_channels()

                channelList = fixtureRequest.get('channels')
                for channel in channelList:
                    chName = channel.get('chName')
                    chValue = channel.get('chValue')
                    logger.debug(f"Channel: {chName}: {chValue}") 
                    self.fixtures[fixtureID].set_channel_data(chName, chValue)

                self.fixtures[fixtureID].update_lighting_data(self.ac)

            self.ac.update()

            fixture_id = data.get('id')

            if data != None:
                return jsonify({'status': 'success'}), 201
            else:
                return jsonify({'error': 'failed to set channels'}), 409

        @self.app.route('/fixtures/flash', methods=['POST'])
        def flash_all_fixtures():
            logger.debug(f"request: flash all fixtures")

            data = request.get_json()
            flashLength = data.get('length')
            flashCycles = data.get('cycles')
            flashDelay = data.get('delay')
   
            for i in range(flashCycles):

                for fixture in self.fixtures.values():
                    fixture.flash(self.ac, flashLength)

                time.sleep(flashDelay/1000)

            if data != None:
                return jsonify({'status': 'success'}), 201
            else:
                return jsonify({'error': 'failed to set channels'}), 409
            
    def run(self, host='0.0.0.0', port=9999):
        logger.debug(f"starting REST server on host {host}:{port}")
        self.app.run(host=host, port=port)

if __name__ == '__main__':
    lighting_rest = LightingREST(None)
    lighting_rest.run()
