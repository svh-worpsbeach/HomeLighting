# Class: Light
# Author: Sven Hapke
# Description: Define a light with a name, a description and several channels
# This code defines a class called 
# Light
#  with several methods. 
#   __init__:       method initializes the object with a name, description, and any number of keyword arguments that represent channels. The 
#   add_channel:    method adds a new channel to the object, the 
#   remove_channel: method removes a channel, the 
#   get_channels:   method returns all channels, and the 
#   get_channel:    method returns a specific channel.

# Assisted by watsonx Code Assistant 

import time

from Channel import Channel

class Fixture:
    def __init__(self, name, description, base_channel, channels):
        self.name = name
        self.description=description
        self.base_channel = base_channel
        self.channels = channels
        self.data = [0] * len(channels)
        self.flashdata = [0] * len(channels)

    def get_name(self):
        return self.name
        
    def add_channel(self, channel):
        self.channels.append ( channel)
        
    def remove_channel(self, channel):
        self.channels.remove (channel)
        
    def get_channels(self):
        return self.channels
    
    def get_channel_by_name(self, name):
        channel = self.channels[name]
        return channel if channel else None
    
    def get_base_channel(self):
        return self.base_channel
    
    def get_channel_offset(self, channel):
        ch = self.channels[channel]

        if ch != None:    
            return ch.get_offset()
        
        return None

    def clear_all_channels(self):
        self.data = [0 for _ in self.data]

    def set_channel_data(self, channel, value):
        self.data[self.get_channel_offset(channel)] = value

        if channel in ['red', 'green', 'blue', 'white', 'amber', 'uv', 'master']:
            if value < 200:
                self.flashdata[self.get_channel_offset(channel)] = 255
            else:
                self.flashdata[self.get_channel_offset(channel)] = 200
    
    def get_fixture_data(self):
        return self.data
    
    def flash(self, lightingDriver, delay):
        lightingDriver.update_data_slots(self.base_channel, self.flashdata) 
        time.sleep(delay/1000)
        lightingDriver.update_data_slots(self.base_channel, self.data) 
        
    def update_lighting_data(self, lightingDriver):
        lightingDriver.update_data_slots(self.base_channel, self.data)
