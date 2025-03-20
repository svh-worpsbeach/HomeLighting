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

    show = None
    fixtures = []
    configData = {}
    ac = None
    showParameter = []
    playLoop = False
    loopCount = None

    def __init__(self, config_file, show):
        if self.is_valid_json_configfile(config_file):

            if ('fixtures' in self.configData):
                self.fixtures = self.read_lights_from_JSON()

        self.show = show
        self.ac = ArtnetConnector()
        self.lightingREST = LightingREST(self.fixtures)
    
    def read_lights_from_JSON(self):
        fixtures = []

        for fixture_data in self.configData['fixtures']:
                    channels = []
                    for channel_data in fixture_data['channels']:
                            functions = []
                            for functions_data in channel_data['functions']:
                                function = Function(functions_data['sequence'], functions_data['description'], functions_data['min_value'], functions_data['max_value'])
                                functions.append(function)
                            channel = Channel(channel_data['name'], channel_data['description'], channel_data['offset'], channel_data['value'], channel_data['type'],functions)
                            channels.append(channel)
                    fixture = Fixture(fixture_data['name'], fixture_data['description'],fixture_data['base_channel'], channels)
                    fixtures.append(fixture)

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

    def setChannel(self, light, channel, value):
            baseChannel = self.lights[light].base_channel
            offset = self.lights[light].get_channel_by_name(channel).get_offset()
            self.ac.setDataSlot(baseChannel+offset, value)

    def setChannelForAll(self, channel, value):
        if len(self.lights) > 0:
            for i in range(len(self.lights)):
                self.setChannel(i, channel, value)

    def flashAllLights(self, delay):
        self.ac.flashAll(delay)
        
    def play_steps_once(self, identifier, delay):
        logger.debug(f"playing {identifier} steps once")

        steps = self.show.get_steps(identifier)

        for s in steps:
             comment = s.get_comment()
             light = s.get_light()
             fixture = self.get_fixture(light)
             base = fixture.get_base_channel()
             
             for set in s.get_settings():
                chName = set.get_name()
                chValue = set.get_value()
                ch = fixture.get_channel_by_name(chName)
                chType = ch.get_type()

                if type(chValue) == 'str':
                    chValue = ch.get_value_by_name(chValue)

                offset = ch.get_offset()

                chValue = ch.verify_function_value(chType, chName, chValue)

                logger.debug(f"setting ch {chName}\t (ch-addr: {base} + {offset})\t --> {chValue}")
                self.ac.setDataSlot(base + offset, chValue)
                time.sleep(delay/1000)

    def play_steps_loop(self, identifier, delay):
        logger.debug(f"starting loop for {identifier} with playLoop set to {self.playLoop}")
        cnt = 0

        if self.show.showType == "loop":
            self.playLoop = True

        while self.playLoop:
            self.play_steps_once(identifier, delay)
            time.sleep(delay/1000)

            if self.loopCount != None:
                cnt += 1
                logger.debug(f"loop count: {cnt}")

                if cnt >= self.loopCount:
                    logger.debug(f"stopping loop at count: {cnt}")
                    self.playLoop = False
             
    def play_steps(self, identifier, delay):
        logger.debug(f"playng steps from {identifier}") 

        if delay > 0:
            delay = self.show.get_Parameter("defaultDelay")
            if self.show.showType == "sequence":
                self.play_steps_once(identifier, delay)
            elif self.show.showType == "loop":
                self.loopCount = self.show.get_Parameter("loopCount")
                self.play_steps_loop(identifier, delay)
        else:
            delay = 0
            self.play_steps_once(identifier, delay)

    def action(self):
        logger.debug("starting show")

        self.play_steps_once('initSteps', 0)

        self.play_steps('showSteps', 1)

        self.play_steps_once('endSteps', 0)

        logger.debug("ending show")


    def start_REST_server(self):
        RESTapi= LightingREST(self)
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
        
