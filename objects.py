from rpython.rlib.objectmodel import r_dict, compute_hash
from rply.token import BaseBox
from errors import *

def dict_eq(key, other):
    # we need to implement rdict method to find key equality
    return key._eq(other)

def dict_hash(key):
    # we need to implement rdict method to find key equality
    return key._hash()


class Null(BaseBox):
    
    def __init__(self):
        pass

    def to_string(self):
        return "<null>"

    def dump(self):
        return "<null>"


class Function(BaseBox):
    
    def __init__(self, name, code):
        self.name = name
        self.code = code
        
    def to_string(self):
        return "<function %s>" % self.name

    def dump(self):
        return "<function %s>" % self.name

    def add(self, right):
        raise Exception("Cannot add that to function %s" % self.name)
    

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
    
    def index(self, right):
        if isinstance(right, Integer):
            return self.values[right.value]
        raise LogicError("Cannot index with that value")
    
    def add(self, right):
    
        if isinstance(right, Array):
            result = Array([])
            result.values.extend(self.values)
            result.values.extend(right.values)
            return result
        raise LogicError("Cannot add that to array")
    
    def sub(self,right):
        if isinstance(right,Integer):
            result = [val for val in self.values]
                
            del result[right.intvalue]
            return Array(result)
        raise LogicError("Cannot remove that index from array")
    
    def to_string(self):
        return '[%s]' % (", ".join(self.map(lambda x: x.to_string(),self.values)))


class Dict(BaseBox):
    
    def __init__(self, args):
        self.values = args
    
    def dump(self):
        return self.to_string()
    
    def map(self, fun, ls):  
        nls = []
        for l in ls:
          nls.append(fun(l))
        return nls
    
    def update(self, key, val):
        self.values[key] = val

    def index(self, right):
        if isinstance(right, Integer):
            return self.values[right]
        if isinstance(right, String):
            return self.values[right]
        if isinstance(right, Float):
            return self.values[right]
        if isinstance(right, Boolean):
            return self.values[right]
        raise LogicError("Cannot index with that value")
    
    def add(self, right):
    
        if isinstance(right, Dict):
            result = Dict(r_dict(dict_eq, dict_hash))
            for key, val in self.values.iteritems():
                result.values[key] = val
            
            for key, val in right.values.iteritems():
                result.values[key] = val

            return result
        raise LogicError("Cannot add that to dict")
    
    def sub(self,right):
        result = r_dict(dict_eq, dict_hash)
        for key, val in self.values.iteritems():
            result[key] = val
            
        del result[right]
        return Dict(result)
    
    def to_string(self):
        return '{%s}' % (", ".join(self.map(lambda k: "%s: %s" % (k[0].to_string(), k[1].to_string()),self.values.iteritems())))


class Boolean(BaseBox):
    
    def __init__(self, value):
        self.boolvalue = bool(value)

    @property
    def value(self):
        return bool(self.boolvalue)

    def __hash__(self):
        return compute_hash(self.boolvalue)

    def __eq__(self, other):
        if(isinstance(other,Boolean)):
            return self.boolvalue == other.boolvalue
        return False

    def _hash(self):
        return compute_hash(self.boolvalue)

    def _eq(self, other):
        if(isinstance(other,Boolean)):
            return self.boolvalue == other.boolvalue
        return False

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

    def __hash__(self):
        return compute_hash(self.intvalue)

    def __eq__(self, other):
        if(isinstance(other,Integer)):
            return (self.intvalue) == (other.intvalue)
        return False

    def _hash(self):
        return compute_hash(self.intvalue)

    def _eq(self, other):
        if(isinstance(other,Integer)):
            return self.intvalue == other.intvalue
        return False

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
        raise LogicError("Cannot add %s to integer" % str(right.__class__.__name__))
    
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
    
    def __hash__(self):
        return compute_hash(self.value)

    def __eq__(self, other):
        return (self.value) == (other.value)
    
    
    def _hash(self):
        return compute_hash(self.floatvalue)

    def _eq(self, other):
        if(isinstance(other,Float)):
            return self.floatvalue == other.floatvalue
        return False
    
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

    def __hash__(self):
        return compute_hash(self.value)

    def __eq__(self, other):
        return (self.value) == (other.value)

    def _hash(self):
        return compute_hash(self.value)

    def _eq(self, other):
        if(isinstance(other,String)):
            return self.value == other.value
        return False

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
    
    def index(self, right):
        if isinstance(right, Integer):
            if right.value >= 0:
                return String(str(self.value[right.value]))
        raise LogicError("Cannot index with that")
    
    def dump(self):
        return str(self.value)


class Variable(BaseBox):
    
    def __init__(self, name, value):
        self.name = str(name)
        self.value = value

    def dump(self):
        return self.value.dump()
