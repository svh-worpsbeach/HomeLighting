# Assisted by watsonx Code Assistant 
from flask import Flask, request, jsonify, make_response

import logging.handlers
import json
import time

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

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
            response = None

            if len(self.fixtures) > 0:
                logger.debug(len(self.fixtures))
                response = make_response (jsonify({'count': len(self.fixtures)}), 201)
            else:
                response = make_response (jsonify({'error': 'no lights defined'}), 404)
        
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response
        
        @self.app.route('/fixtures/names', methods=['GET'])
        def get_light_names():
            logger.debug(f"request: light names")
            response = None

            names = list(self.fixtures.keys())

            jsonResp = '['

            count = 0

            for name in names:

                jsonResp = jsonResp + "{"
                jsonResp = jsonResp + f"\"id\": \"{count}\"," 
                jsonResp = jsonResp + f"\"name\": \"{name}\"" 
                jsonResp = jsonResp + "},"

                count += 1

            jsonResp = jsonResp[:-1]

            jsonResp = jsonResp + "]"

            if len(names) > 0:
                logger.debug(jsonify(jsonResp))
                response = make_response (jsonify(jsonResp), 201)
            else:
                response = make_response (jsonify({'error': 'no fixtures defined'}), 404)
            
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response

        @self.app.route('/fixtures/blackout', methods=['GET'])
        def black_out_fixtures():
            logger.debug(f"request: blank")
            response = None

            if self.ac.blackout_all_fixtures():
                response = jsonify({'status': 'success'}), 201
            else:
                response = jsonify({'error': 'blanking did not work'}), 404
            
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response

        @self.app.route('/fixtures/<string:fixture_id>', methods=['GET'])
        def get_light_status(fixture_id):
            logger.debug(f"request: light defnition of {fixture_id}")
            response = None

            fixture = self.fixtures[fixture_id]

            if fixture != None:
                logger.debug(fixture)
                json_data = json.dumps(fixture, default=lambda o: o.__dict__, indent=4)
                logger.debug(json_data)
                response = make_response (jsonify(json_data), 201)
            else:
                response = make_response (jsonify({'error': 'Fixture not found'}), 404)

            response.headers.add("Access-Control-Allow-Origin", "*")
            return response
        
        @self.app.route('/fixture/setchannel', methods=['POST'])
        def set_fixture_channel():
            logger.debug(f"request: set channels for fixtures")
            response 

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
                response = make_response (jsonify({'status': 'success'}), 201)
            else:
                response = make_response (jsonify({'error': 'failed to set channels'}), 409)

            response.headers.add("Access-Control-Allow-Origin", "*")
            return response
        
        @self.app.route('/fixtures/flash', methods=['POST'])
        def flash_all_fixtures():
            logger.debug(f"request: flash all fixtures")
            response = None

            data = request.get_json()
            flashLength = data.get('length')
            flashCycles = data.get('cycles')
            flashDelay = data.get('delay')
   
            for i in range(flashCycles):

                for fixture in self.fixtures.values():
                    fixture.flash(self.ac, flashLength)

                time.sleep(flashDelay/1000)

            if data != None:
                response = make_response (jsonify({'status': 'success'}), 201)
            else:
                response = make_response (jsonify({'error': 'failed to set channels'}), 409)
            
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response
        
    def run(self, host='0.0.0.0', port=9999):
        logger.debug(f"starting REST server on host {host}:{port}")
        self.app.run(host=host, port=port)

if __name__ == '__main__':
    lighting_rest = LightingREST(None)
    lighting_rest.run()
