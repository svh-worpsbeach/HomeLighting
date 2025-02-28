# This code defines a class called 
# Channel
# with four attributes: 
# name, description, id and value. 
# The 
# __init__: method is a special method in Python classes that is called when an object is created. It initializes the attributes of the object with the values passed as arguments.

# Assisted by watsonx Code Assistant 
class Channel:
    def __init__(self, name, description, offset, value, functions):
        self.name = name
        self.description = description
        self.offset = offset
        self.value = value
        self.functions = functions

    def get_name(self):
        return self.name

    def get_description(self):
        return self.description

    def get_offset(self):
        return self.offset

    def get_value(self):
        return self.value