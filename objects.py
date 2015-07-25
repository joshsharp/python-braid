from rply.token import BaseBox

class Null(BaseBox):
    
    def __init__(self):
        pass

    def to_string(self):
        return "(null)"

    def dump(self):
        return "null"

class Boolean(BaseBox):
    
    def __init__(self, value):
        self.value = bool(value)

    def to_string(self):
        return str(self.value).lower()
    
    def equals(self, right):
        if type(right) is Boolean:
            return Boolean(self.value == right.value)
        if type(right) is Integer:
            return Boolean(self.to_int() == right.value)
        if type(right) is Float:
            return Boolean(self.to_int() == right.value)
        else:
            return Boolean(False)
        raise LogicError("Cannot compare that to boolean")
    
    def lte(self, right):
        if type(right) is Boolean:
            return Boolean(self.value == right.value)
        raise LogicError("Cannot compare that to boolean")
    
    def lt(self, right):
        raise LogicError("Cannot compare boolean that way")
    
    def gt(self, right):
        raise LogicError("Cannot compare boolean that way")
    
    def gte(self, right):
        if type(right) is Boolean:
            return Boolean(self.value == right.value)
        raise LogicError("Cannot compare that to boolean")
    
    def add(self, right):
        raise LogicError("Cannot add that to boolean")
    
    def sub(self, right):
        raise LogicError("Cannot sub that from boolean")
    
    def mul(self, right):
        raise LogicError("Cannot mul that to boolean")
    
    def div(self, right):
        raise LogicError("Cannot div that from boolean")
    
    def to_string(self):
        if self.value:
            return "true"
        return "false"

    def to_int(self):
        if self.value:
            return 1
        return 0
    
    def dump(self):
        return str(self.value)

class Integer(BaseBox):
    
    def __init__(self, value):
        self.value = int(value)

    def to_string(self):
        return str(self.value)

    def dump(self):
        return str(self.value)
    
    def equals(self, right):
        if type(right) is Float:
            return Boolean(self.value == right.value)
        if type(right) is Integer:
            return Boolean(self.value == right.value)
        if type(right) is Boolean:
            return Boolean(self.value == right.to_int())
        raise LogicError("Cannot compare that to integer")
    
    def lte(self, right):
        if type(right) is Integer:
            return Boolean(self.value <= right.value)
        if type(right) is Float:
            return Boolean(self.value <= right.value)
        raise LogicError("Cannot compare that to integer")
    
    def lt(self, right):
        if type(right) is Integer:
            return Boolean(self.value < right.value)
        if type(right) is Float:
            return Boolean(self.value < right.value)
        raise LogicError("Cannot compare integer that way")
    
    def gt(self, right):
        if type(right) is Integer:
            return Boolean(self.value > right.value)
        if type(right) is Float:
            return Boolean(self.value > right.value)
        raise LogicError("Cannot compare integer that way")
    
    def gte(self, right):
        if type(right) is Integer:
            return Boolean(self.value >= right.value)
        if type(right) is Float:
            return Boolean(self.value >= right.value)
        raise LogicError("Cannot compare integer that way")
    
    def add(self, right):
    
        if type(right) is Integer:
            return Integer(self.value + right.value)
        if type(right) is Float:
            return Float(self.value + right.value)
        raise LogicError("Cannot add that to integer")
    
    def sub(self, right):
        if type(right) is Integer:
            return Integer(self.value - right.value)
        if type(right) is Float:
            return Float(self.value - right.value)
        raise LogicError("Cannot sub from int")
    
    def mul(self, right):
        if type(right) is Integer:
            return Integer(self.value * right.value)
        if type(right) is Float:
            return Float(self.value * right.value)
        raise LogicError("Cannot mul that to int")
    
    def div(self, right):
        if type(right) is Integer:
            return Integer(self.value / right.value)
        if type(right) is Float:
            return Float(self.value / right.value)
        raise LogicError("Cannot div that with int")

    
class Float(BaseBox):
    
    def __init__(self, value):
        self.value = float(value)
    def equals(self, right):
        if type(right) is Float:
            return Boolean(self.value == right.value)
        if type(right) is Integer:
            return Boolean(self.value == right.value)
        if type(right) is Boolean:
            return Boolean(self.value == right.to_int())
        raise LogicError("Cannot compare that to float")
    
    def lte(self, right):
        if type(right) is Integer:
            return Boolean(self.value <= right.value)
        if type(right) is Float:
            return Boolean(self.value <= right.value)
        raise LogicError("Cannot compare that to integer")
    
    def lt(self, right):
        if type(right) is Integer:
            return Boolean(self.value < right.value)
        if type(right) is Float:
            return Boolean(self.value < right.value)
        raise LogicError("Cannot compare integer that way")
    
    def gt(self, right):
        if type(right) is Integer:
            return Boolean(self.value > right.value)
        if type(right) is Float:
            return Boolean(self.value > right.value)
        raise LogicError("Cannot compare integer that way")
    
    def gte(self, right):
        if type(right) is Integer:
            return Boolean(self.value >= right.value)
        if type(right) is Float:
            return Boolean(self.value >= right.value)
        raise LogicError("Cannot compare integer that way")
    
    def add(self, right):
    
        if type(right) is Integer:
            return Float(self.value + right.value)
        if type(right) is Float:
            return Float(self.value + right.value)
        raise LogicError("Cannot add that to float")
    
    def sub(self, right):
        if type(right) is Float:
            return Float(self.value - right.value)
        if type(right) is Integer:
            return Float(self.value - right.value)
        raise LogicError("Cannot sub string")
    
    def mul(self, right):
        if type(right) is Integer:
            return Float(self.value * right.value)
        if type(right) is Float:
            return Float(self.value * right.value)
        raise LogicError("Cannot mul that to float")
    
    def div(self, right):
        if type(right) is Integer:
            return Float(self.value / right.value)
        if type(right) is Float:
            return Float(self.value / right.value)
        raise LogicError("Cannot div that with float")

    def dump(self):
        return str(self.value)

class String(BaseBox):
    
    def __init__(self, value):
        self.value = str(value)

    def to_string(self):
        return str(self.value)
    
    def equals(self, right):
        if type(right) is String:
            return Boolean(self.value == right.value)
        if type(right) is Boolean:
            length = int(len(self.value) != 0)
            return Boolean(length == right.to_int())
        raise LogicError("Cannot compare that to string")
    
    def lte(self, right):
        if type(right) is String:
            return Boolean(self.value == right.value)
        raise LogicError("Cannot compare that to string")
    
    def lt(self, right):
        raise LogicError("Cannot compare string that way")
    
    def gt(self, right):
        raise LogicError("Cannot compare string that way")
    
    def gte(self, right):
        if type(right) is String:
            return Boolean(self.value == right.value)
        raise LogicError("Cannot compare that to string")
    
    def add(self, right):
    
        if type(right) is Integer:
            return String(self.value + str(right.value))
        if type(right) is Float:
            return String(self.value + str(right.value))
        if type(right) is String:
            return String(self.value + right.value)
        raise LogicError("Cannot add that to string")
    
    def sub(self, right):
        if type(right) is Integer:
            
            sli = len(self.value) - right.value
            assert(sli >= 0)
            return String(self.value[:sli])
        if type(right) is Float:
            
            sli = len(self.value) - int(right.value)
            assert(sli >= 0)
            return String(self.value[:sli])
        raise LogicError("Cannot sub string")
    
    def mul(self, right):
        if type(right) is Integer:
            return String(self.value * right.value)
        if type(right) is Float:
            return String(self.value * int(right.value))
        raise LogicError("Cannot multiply string with that")
    
    def div(self, right):
        raise LogicError("Cannot divide a string")
    
    def index(self, value):
        if type(value) is Integer:
            if value.value >= 0:
                return String(str(self.value[value.value]))
        raise LogicError("Cannot index with that")
    
    def dump(self):
        return str(self.value)
