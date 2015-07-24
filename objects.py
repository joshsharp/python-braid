from rply.token import BaseBox

class Null(BaseBox):
    
    def __init__(self):
        pass

    def dump(self):
        return "null"

class Boolean(BaseBox):
    
    def __init__(self, value):
        self.value = bool(value)

    def dump(self):
        return str(self.value)

class Integer(BaseBox):
    
    def __init__(self, value):
        self.value = int(value)

    def dump(self):
        return str(self.value)
    
class Float(BaseBox):
    
    def __init__(self, value):
        self.value = float(value)

    def dump(self):
        return str(self.value)

class String(BaseBox):
    
    def __init__(self, value):
        self.value = str(value)

    def dump(self):
        return str(self.value)
