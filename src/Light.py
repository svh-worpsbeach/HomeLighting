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

from Channel import Channel

class Light:
    def __init__(self, name, description, base_channel, channels):
        self.name = name
        self.description=description
        self.base_channel = base_channel
        self.channels = channels
        
    def add_channel(self, channel):
        self.channels.append ( channel)
        
    def remove_channel(self, channel):
        self.channels.remove (channel)
        
    def get_channels(self):
        return self.channels
    
    def get_channel_by_name(self, name):
        channel = [ch for ch in self.channels if ch.name == name]
        return channel[0] if channel else None