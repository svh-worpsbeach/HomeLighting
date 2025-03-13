from Setting import Setting

class Step:
    comment = None
    light = None
    settings = []

    def __init__(self, comment, light, settings):
        self.comment = comment
        self.light = light
        self.settings = settings


    def get_comment(self):
        return self.comment
    
    def get_light(self):
        return self.light
    
    def get_settings(self):
        return self.settings