# This code defines a class called 
# Channel
# with four attributes: 
# name, description, id and value. 
# The 
# __init__: method is a special method in Python classes that is called when an object is created. It initializes the attributes of the object with the values passed as arguments.

# Assisted by watsonx Code Assistant 
class Channel:
    def __init__(self, name, description, offset, value, type, functions):
        self.name = name
        self.description = description
        self.offset = offset
        self.value = value
        self.type=type
        self.functions = functions

    def get_name(self):
        return self.name
    
    def get_type(self):
        return self.type

    def get_description(self):
        return self.description

    def get_offset(self):
        return self.offset

    def get_value(self):
        return self.value
    
    def get_function(self, identifier):
        function = None

        if len(self.functions) > 1:
            for f in self.functions:
                if f.get_desc() == identifier:
                    function = f
                    pass
        else:
            function = self.functions[0]

        return function
    
    def get_value_by_name(self, identifier):
        val = 0
    
        if len(self.functions) > 1:
            for f in self.functions:
                if f.get_desc().lower() == identifier.lower():
                    fMin = f.getMin()
                    fMax = f.getMax()
                    val = fMin + ((fMax-fMin)/2)
                    pass
        else:
            f = self.functions[0]
            fMin = f.getMin()
            fMax = f.getMax()
            val = fMin + ((fMax-fMin)/2)
            pass

        return val
    
    def verify_function_value(self, chtype, name, value):
        val = None

        if chtype == "presets":
            name = value

        function = self.get_function(name)
        
        funcMin = function.get_min()
        funcMax = function.get_max()

        if type(value) == int:
            if (value >= funcMin) & (value <= funcMax):
                val = value
        elif type(value) == str:
            
            val = (funcMin + ((funcMax - funcMin)//2))

        return val