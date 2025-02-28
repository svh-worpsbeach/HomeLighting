# Assisted by watsonx Code Assistant 
class Function:
    def __init__(self, seq, desc, min, max):
        self.seq = seq
        self.desc = desc

        if min < max:
            if min >= 0:
                self.min = min
            else:
                self.min = 0

            if max <= 255:
                self.max = max
            else:
                self.max = 255
        else:
            self.min = 0
            self.max = 255
        
        self.max = max

    def get_seq(self):
        return self.seq

    def get_desc(self):
        return self.desc

    def get_min(self):
        return self.min

    def get_max(self):
        return self.max

