from rply.token import BaseBox
from errors import *

class Null(BaseBox):
    
    def __init__(self):
        pass

    def to_string(self):
        return "(null)"

    def dump(self):
        return "null"


class Function(BaseBox):
    
    def __init__(self, name, args, block):
        self.name = name
        self.args = args
        self.block = block
    
    def to_string(self):
        return "(function)"

    def dump(self):
        return "function"


class Array(BaseBox):
    
    def __init__(self, args):
        self.values = args
    
    def dump(self):
        return self.to_string()
    
    def map(self, fun, ls):  
        nls = []
        for l in ls:
          nls.append(fun(l))
        return nls
    
    def push(self, statement):
        self.values.insert(0,statement)
    
    def append(self, statement):
        self.values.append(statement)
    
    def index(self, i):
        if type(i) is Integer:
            return self.values[i.value]
        raise LogicError("Cannot index with that value")
    
    def add(self, right):
    
        if type(right) is Array:
            result = Array([])
            result.values.extend(self.values)
            result.values.extend(right.values)
            return result
        raise LogicError("Cannot add that to array")
    
    def to_string(self):
        return '[%s]' % (", ".join(self.map(lambda x: x.to_string(),self.values)))


class Boolean(BaseBox):
    
    def __init__(self, value):
        self.boolvalue = bool(value)

    @property
    def value(self):
        return bool(self.boolvalue)

    def equals(self, right):
        if isinstance(right, Boolean):
            return Boolean(self.value == right.value)
        if isinstance(right, Integer):
            return Boolean(self.to_int() == right.value)
        if isinstance(right, Float):
            return Boolean(self.to_int() == right.value)
        else:
            return Boolean(False)
        raise LogicError("Cannot compare that to boolean")
    
    def lte(self, right):
        if isinstance(right, Boolean):
            return Boolean(self.value == right.value)
        raise LogicError("Cannot compare that to boolean")
    
    def lt(self, right):
        raise LogicError("Cannot compare boolean that way")
    
    def gt(self, right):
        raise LogicError("Cannot compare boolean that way")
    
    def gte(self, right):
        if isinstance(right, Boolean):
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
        return self.to_string()

class Integer(BaseBox):
    
    def __init__(self, value):
        self.intvalue = int(value)

    @property
    def value(self):
        return int(self.intvalue)

    def to_string(self):
        return str(self.value)

    def dump(self):
        return str(self.value)
    
    def equals(self, right):
        if isinstance(right,Float):
            return Boolean(float(self.value) == right.value)
        if isinstance(right, Integer):
            return Boolean(self.value == right.value)
        if isinstance(right, Boolean):
            return Boolean(self.value == right.to_int())
        raise LogicError("Cannot compare that to integer")
    
    def lte(self, right):
        if isinstance(right, Integer):
            return Boolean(self.value <= right.value)
        if isinstance(right,Float):
            return Boolean(float(self.value) <= right.value)
        raise LogicError("Cannot compare that to integer")
    
    def lt(self, right):
        if isinstance(right, Integer):
            return Boolean(self.value < right.value)
        if type(right) is Float:
            return Boolean(float(self.value) < right.value)
        raise LogicError("Cannot compare integer that way")
    
    def gt(self, right):
        if isinstance(right, Integer):
            return Boolean(self.value > right.value)
        if isinstance(right,Float):
            return Boolean(float(self.value) > right.value)
        raise LogicError("Cannot compare integer that way")
    
    def gte(self, right):
        if isinstance(right, Integer):
            return Boolean(self.value >= right.value)
        if isinstance(right,Float):
            return Boolean(float(self.value) >= right.value)
        raise LogicError("Cannot compare integer that way")
    
    def add(self, right):
    
        if isinstance(right, Integer):
            return Integer(self.value + right.value)
        if isinstance(right,Float):
            return Float(float(self.value) + right.value)
        raise LogicError("Cannot add that to integer")
    
    def sub(self, right):
        if isinstance(right, Integer):
            return Integer(self.value - right.value)
        if isinstance(right,Float):
            return Float(float(self.value) - right.value)
        raise LogicError("Cannot sub from int")
    
    def mul(self, right):
        if isinstance(right, Integer):
            return Integer(self.value * right.value)
        if isinstance(right,Float):
            return Float(float(self.value) * right.value)
        raise LogicError("Cannot mul that to int")
    
    def div(self, right):
        if isinstance(right, Integer):
            return Integer(self.value / right.value)
        if isinstance(right,Float):
            return Float(float(self.value) / right.value)
        raise LogicError("Cannot div that with int")

    
class Float(BaseBox):
    
    def __init__(self, val):
        self.floatvalue = float(val)

    @property
    def value(self):
        return float(self.floatvalue)
    
    def to_string(self):
        return str(self.value)
    
    def equals(self, right):
        
        if isinstance(right,Float):
            return Boolean(self.value == right.value)
        if isinstance(right, Integer):
            return Boolean(self.value == float(right.value))
        if isinstance(right, Boolean):
            return Boolean(self.value == float(right.to_int()))
        raise LogicError("Cannot compare that to float")
    
    def lte(self, right):
        
        if isinstance(right, Integer):
            return Boolean(self.value <= float(right.value))
        if isinstance(right,Float):
            return Boolean(self.value <= right.value)
        raise LogicError("Cannot compare that to integer")
    
    def lt(self, right):
        
        if isinstance(right, Integer):
            return Boolean(self.value < float(right.value))
        if type(right) is Float:
            return Boolean(self.value < right.value)
        raise LogicError("Cannot compare integer that way")
    
    def gt(self, right):
        
        if isinstance(right, Integer):
            return Boolean(self.value > float(right.value))
        if isinstance(right,Float):
            return Boolean(self.value > right.value)
        raise LogicError("Cannot compare integer that way")
    
    def gte(self, right):
        
        if isinstance(right, Integer):
            return Boolean(self.value >= float(right.value))
        if isinstance(right,Float):
            return Boolean(self.value >= right.value)
        raise LogicError("Cannot compare integer that way")
    
    def add(self, right):
        
        if isinstance(right, Integer):
            return Float(self.value + float(right.value))
        if isinstance(right,Float):
            return Float(self.value + right.value)
        raise LogicError("Cannot add that to float")
    
    def sub(self, right):
        
        if isinstance(right,Float):
            return Float(self.value - right.value)
        if isinstance(right, Integer):
            return Float(self.value - float(right.value))
        raise LogicError("Cannot sub string")
    
    def mul(self, right):
        
        if isinstance(right, Integer):
            return Float(self.value * float(right.value))
        if isinstance(right,Float):
            return Float(self.value * right.value)
        raise LogicError("Cannot mul that to float")
    
    def div(self, right):
        
        if isinstance(right, Integer):
            return Float(self.value / float(right.value))
        if isinstance(right,Float):
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
        if isinstance(right, String):
            return Boolean(self.value == right.value)
        if isinstance(right, Boolean):
            length = int(len(self.value) != 0)
            return Boolean(length == right.to_int())
        raise LogicError("Cannot compare that to string")
    
    def lte(self, right):
        if isinstance(right, String):
            return Boolean(self.value == right.value)
        raise LogicError("Cannot compare that to string")
    
    def lt(self, right):
        raise LogicError("Cannot compare string that way")
    
    def gt(self, right):
        raise LogicError("Cannot compare string that way")
    
    def gte(self, right):
        if isinstance(right, String):
            return Boolean(self.value == right.value)
        raise LogicError("Cannot compare that to string")
    
    def add(self, right):
    
        if isinstance(right, Integer):
            return String(self.value + str(right.value))
        if isinstance(right,Float):
            return String("%s%s" % (self.value,right.value))
        if isinstance(right, String):
            return String(self.value + right.value)
        raise LogicError("Cannot add that to string")
    
    def sub(self, right):
        if isinstance(right, Integer):
            
            sli = len(self.value) - right.value
            assert(sli >= 0)
            return String(self.value[:sli])
        
        raise LogicError("Cannot sub string")
    
    def mul(self, right):
        if isinstance(right, Integer):
            return String(self.value * right.value)
        
        raise LogicError("Cannot multiply string with that")
    
    def div(self, right):
        raise LogicError("Cannot divide a string")
    
    def index(self, value):
        if isinstance(right, Integer):
            if value.value >= 0:
                return String(str(self.value[value.value]))
        raise LogicError("Cannot index with that")
    
    def dump(self):
        return str(self.value)


class Variable(BaseBox):
    
    def __init__(self, name, value):
        self.name = str(name)
        self.value = value

    def dump(self):
        return "Variable %s" % str(self.name)
