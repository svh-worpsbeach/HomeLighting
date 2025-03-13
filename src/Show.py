import json

from Step import Step
from Setting import Setting

class Show:

    showType = None # can be "loop", "sequence" or "default"
    showParameters = [] 
    initSteps = []
    endSteps = []
    showSteps = []

    def __init__(self, showFile):    
        if self.is_valid_json_showfile(showFile):
            if ('parameter' in self.showData):
                self.showType = self.showData['type']
                self.showParameters = []
                for param_data in self.showData['parameter']:
                    setting = Setting(param_data['name'], param_data['value'])
                    self.showParameters.append(setting)
            
            if ('initShow' in self.showData):
                self.initSteps = self.read_steps_from_JSON('initShow')

            if ('endShow' in self.showData):
                self.endSteps = self.read_steps_from_JSON('endShow')

            if ('showSteps' in self.showData):    
                self.showSteps = self.read_steps_from_JSON('showSteps')

    def get_Parameter(self, parameterID):
        param = None

        for p in self.showParameters:
            if p.name == parameterID:
                param = p.value

        return param

    def is_valid_json_showfile(self, file_path):
        try:
            with open(file_path) as f:
                self.showData = json.load(f)
            return True
        except ValueError:
            return False
        
    def read_steps_from_JSON(self, section):
        steps = []
        for data in self.showData[section]:
            settings = []
            for setting_data in data['settings']:
                setting = Setting(setting_data['name'], setting_data['value'])
                settings.append(setting)

            step = Step(data['Comment'], data['light'], settings )
            steps.append(step)

        return steps
    
    def get_steps(self, identifier):
        if identifier == "initSteps":
            return self.initSteps
        elif identifier == 'endSteps':
            return self.endSteps
        elif identifier == 'showSteps':
            return self.showSteps

        
