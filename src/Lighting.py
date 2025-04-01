import json 
import time
import sys

from Fixture import Fixture
from Channel import Channel
from Function import Function
from Show import Show

from ArtnetConnector import ArtnetConnector
from LightingREST import LightingREST

import logging.handlers
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class Lighting:

    # show = None
    fixtures = []
    configData = {}
    ac = None
    showParameter = []
    playLoop = False
    loopCount = None

    def __init__(self, config_file):
        logger.debug(f"Initialize {__name__}")

        if self.is_valid_json_configfile(config_file):

            if ('fixtures' in self.configData):
                self.fixtures = self.read_lights_from_JSON()

        # self.show = show
        self.ac = ArtnetConnector()
        self.lightingREST = LightingREST(self.fixtures, self.ac)
    
    def read_lights_from_JSON(self):
        fixtures = {}

        for fixture_data in self.configData['fixtures']:
                    channels = {}
                    for channel_data in fixture_data['channels']:
                            functions = {}
                            for functions_data in channel_data['functions']:
                                function = Function(functions_data['sequence'], functions_data['description'], functions_data['min_value'], functions_data['max_value'])
                                functions[function.get_desc()] = function
                            channel = Channel(channel_data['name'], channel_data['description'], channel_data['offset'], channel_data['value'], channel_data['type'],functions)
                            channels[channel.get_name()] = channel
                    fixture = Fixture(fixture_data['name'], fixture_data['description'],fixture_data['base_channel'], channels)
                    fixtures[fixture.get_name()] = fixture

        return fixtures

    def is_valid_json_configfile(self, file_path):
        try:
            with open(file_path) as f:
                self.configData = json.load(f)
            return True
        except ValueError:
            return False
    
    def setMasterDimmer(self, light, value):
        ch = self.lights[light].get_channel_by_name("master")
        if ch != None:
            offset = ch.get_offset()
            baseChannel = self.lights[light].base_channel
            self.ac.setDataSlot(baseChannel+offset, value)

    def setAllDimmer(self, value):
        if len(self.lights) > 0:
            for i in range(len(self.lights)):
                self.setMasterDimmer(i, value)

    # Assisted by watsonx Code Assistant 
    def setChannel(self, light, channel, value):
        """
        Set the value of a specific channel for a given light.
    
        Args:
            light (str): The name of the light.
            channel (str): The name of the channel.
            value (int): The value to set the channel to.
    
        Returns:
            None
        """
        baseChannel = self.lights[light].base_channel
        offset = self.lights[light].get_channel_by_name(channel).get_offset()
        self.ac.setDataSlot(baseChannel+offset, value)
    
    def setChannelForAll(self, channel, value):
        if len(self.lights) > 0:
            for i in range(len(self.lights)):
                self.setChannel(i, channel, value)

    def flashAllLights(self, delay):
        self.ac.flashAll(delay)
        
    def action(self):
        logger.debug("starting show")

        self.play_steps_once('initSteps', 0)

        self.play_steps('showSteps', 1)

        self.play_steps_once('endSteps', 0)

        logger.debug("ending show")

    def start_REST_server(self):
        RESTapi= LightingREST(self, self.ac)
        self.lightingREST.run()
        
    def default_action(self):

        self.setAllDimmer(128)
        
        if (len(self.lights) > 0):

        
            print ("Red 1:")
            print (self.lights[0].get_channel_by_name("red").value)

            print ("Red 2:")
            print (self.lights[1].get_channel_by_name("red").value)

            self.lights[1].get_channel_by_name("red").value = 99
            self.setChannel(0, "presets", 155)
            self.setChannel(1, "red", 99)
            time.sleep(3)

            self.flashAllLights(1)

            self.flashAllLights(1)

            print ("Red 1:")
            print (self.lights[0].get_channel_by_name("red").value)

            print ("Red 2:")
            print (self.lights[1].get_channel_by_name("red").value)
        else:
            print ("No lights defined")

        time.sleep(10)

        self.setAllDimmer(0)
        
