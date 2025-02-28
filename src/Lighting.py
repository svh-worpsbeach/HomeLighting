import json 
import time

from Light import Light
from Channel import Channel
from Function import Function

#import sys
#raise RuntimeError(sys.path)

from ArtnetConnector import ArtnetConnector

class Lighting:

    lights = []
    configData = {}
    ac = None

    def __init__(self, config_file):
        if self.is_valid_json_file(config_file):

            if ('lights' in self.configData):
                for light_data in self.configData['lights']:
                    channels = []
                    for channel_data in light_data['channels']:
                            functions = []
                            for functions_data in channel_data['functions']:
                                function = Function(functions_data['sequence'], functions_data['description'], functions_data['min_value'], functions_data['max_value'])
                                functions.append(function)
                            channel = Channel(channel_data['name'], channel_data['description'], channel_data['offset'], channel_data['value'], functions)
                            channels.append(channel)
                    light = Light(light_data['name'], light_data['description'],light_data['base_channel'], channels)
                    self.lights.append(light)

        self.ac = ArtnetConnector()

    def is_valid_json_file(self, file_path):
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
        
    def action(self):

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
        
