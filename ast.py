from rply.token import BaseBox
from errors import *

# all token types inherit rply's basebox as rpython needs this
# these classes represent our Abstract Syntax Tree
class Program(BaseBox):
    
    def __init__(self, statement):
        self.statements = []
        self.statements.append(statement)
    
    def add_statement(self, statement):
        self.statements.insert(0,statement)
        
    def eval(self, env):
        #print "count: %s" % len(self.statements)
        result = None
        for statement in self.statements:
            result = statement.eval(env)
            #print result.to_string()
        return result
    
    def rep(self):
        result = 'Program('
        for statement in self.statements:
            result += statement.rep()
        result += ')'
        return result


class Block(BaseBox):
    
    def __init__(self, statement):
        self.statements = []
        self.statements.append(statement)
    
    def add_statement(self, statement):
        self.statements.insert(0,statement)
        
    def eval(self, env):
        #print "count: %s" % len(self.statements)
        result = None
        for statement in self.statements:
            result = statement.eval(env)
            #print result.to_string()
        return result
    
    def rep(self):
        result = 'Block('
        for statement in self.statements:
            result += statement.rep()
        result += ')'
        return result

class Array(BaseBox):
    
    def map(self, fun, ls):  
        nls = []
        for l in ls:
          nls.append(fun(l))
        return nls
    
    def __init__(self, statement):
        self.statements = []
        self.values = []
        self.statements.append(statement)
    
    def push(self, statement):
        self.statements.insert(0,statement)
    
    def append(self, statement):
        self.statements.append(statement)
        
    def eval(self, env):
        #print "count: %s" % len(self.statements)
        
        if len(self.values) == 0:            
            for statement in self.statements:
                self.values.append(statement.eval(env))
                #print result.to_string()
        return self
    
    def rep(self):
        result = 'Array('
        result += ",".join(self.map(lambda x: x.rep(),self.statements))
        result += ')'
        return result
    
    def to_string(self):
        return '[%s]' % (", ".join(self.map(lambda x: x.to_string(),self.values)))

class Null(BaseBox):
    
    def eval(self, env):
        return self
    
    def to_string(self):
        return 'null'

    def rep(self):
        return 'Null()'


class Boolean(BaseBox):
    def __init__(self, value):
        self.value = bool(value)

    def eval(self, env):
        return self
    
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
    
    def rep(self):
        return 'Boolean(%s)' % self.value


class Integer(BaseBox):
    def __init__(self, value):
        self.value = int(value)

    def eval(self, env):
        return self
    
    def to_string(self):
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

    def rep(self):
        return 'Integer(%s)' % self.value


class Float(BaseBox):
    def __init__(self, value):
        self.value = float(value)

    def eval(self, env):
        return self

    def to_string(self):
        return str(self.value)

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

    def rep(self):
        return 'Float(%s)' % self.value


class String(BaseBox):
    def __init__(self, value):
        self.value = str(value)

    def eval(self, env):
        return self

    def to_string(self):
        return '"%s"' % str(self.value)

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
    
    def rep(self):
        return 'String(%s)' % self.value
        
    
class Variable(BaseBox):
    def __init__(self, name):
        self.name = name
        self.value = None

    def getname(self):
        return self.name

    def eval(self, env):
        if env.variables.get(self.name, None) is not None:
            self.value = env.variables[self.name].eval(env)
            return self.value
        raise LogicError("Not yet defined")
    
    def to_string(self):
        return str(self.name)
    
    def equals(self, right):
        return self.value.equals(right)
    
    def add(self, right):
        return self.value.add(right)
    
    def sub(self, right):
        return self.value.sub(right)
    
    def mul(self, right):
        return self.value.mul(right)
    
    def div(self, right):
        return self.value.div(right)

    def rep(self):
        return 'Variable(%s)' % self.name
        

class Print(BaseBox):
    def __init__(self, value):
        self.value = value
    
    def eval(self, env):
        print self.value.eval(env).to_string()
        return self.value.eval(env) 
    
    def to_string(self):
        return "Print"

    def rep(self):
        return "Print(%s)" % self.value.rep()


class If(BaseBox):
    def __init__(self, condition, body, else_body=Null()):
        self.condition = condition
        self.body = body
        self.else_body = else_body
        
    def eval(self, env):
        condition = self.condition.eval(env)
        if Boolean(True).equals(condition).value:
            
            return self.body.eval(env)
        else:
            
            if type(self.else_body) is not Null:
                return self.else_body.eval(env)
        return Null()

    def rep(self):
        return 'If(%s) Then(%s) Else(%s)' % (self.condition.rep(), self.body.rep(), self.else_body.rep())


class BinaryOp(BaseBox):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    
    def to_string(self):
        return 'BinaryOp'
    
    def rep(self):
        return  'BinaryOp(%s, %s)' % (self.left.rep(), self.right.rep())


class Equal(BinaryOp):
    
    def rep(self):
        return 'Equal(%s, %s)' % (self.left.rep(), self.right.rep())
    
    def eval(self, env):
        return self.left.eval(env).equals(self.right.eval(env))


class NotEqual(BinaryOp):
    
    def rep(self):
        return 'NotEqual(%s, %s)' % (self.left.rep(), self.right.rep())
    
    def eval(self, env):
        result = self.left.eval(env).equals(self.right.eval(env))
        result.value = not result.value
        return result


class GreaterThan(BinaryOp):
    
    def rep(self):
        return 'GreaterThan(%s, %s)' % (self.left.rep(), self.right.rep())
    
    def eval(self, env):
        return self.left.eval(env).gt(self.right.eval(env))


class LessThan(BinaryOp):
    
    def rep(self):
        return 'LessThan(%s, %s)' % (self.left.rep(), self.right.rep())
    
    def eval(self, env):
        return self.left.eval(env).lt(self.right.eval(env))


class GreaterThanEqual(BinaryOp):
    
    def rep(self):
        return 'GreaterThan(%s, %s)' % (self.left.rep(), self.right.rep())
    
    def eval(self, env):
        return self.left.eval(env).gte(self.right.eval(env))


class LessThanEqual(BinaryOp):
    
    def rep(self):
        return 'LessThan(%s, %s)' % (self.left.rep(), self.right.rep())
    
    def eval(self, env):
        return self.left.eval(env).lte(self.right.eval(env))


class Add(BinaryOp):
    
    def rep(self):
        return  'Add(%s, %s)' % (self.left.rep(), self.right.rep())
    
    def eval(self, env):
        # this needs to call 'add' or something on the left, passing in the right
        # cannot check that types are 'primitives' eg. Float like we were doing
        # because compound expression like 5 + 5 + 5 will end up with
        # Add(Float,Add(Float)) tree.
        
        return self.left.eval(env).add(self.right.eval(env))
        
class Sub(BinaryOp):
    
    def rep(self):
        return  'Sub(%s, %s)' % (self.left.rep(), self.right.rep())
    
    def eval(self, env):
        return self.left.eval(env).sub(self.right.eval(env))
        
        
class Mul(BinaryOp):
    
    def rep(self):
        return  'Mul(%s, %s)' % (self.left.rep(), self.right.rep())
    
    def eval(self, env):
        return self.left.eval(env).mul(self.right.eval(env))
        
class Div(BinaryOp):
    def rep(self):
        return  'Div(%s, %s)' % (self.left.rep(), self.right.rep())
    
    def eval(self, env):
        return self.left.eval(env).div(self.right.eval(env))

class Assignment(BinaryOp):
    
    def rep(self):
        return  'Assignment(%s, %s)' % (self.left.rep(), self.right.rep())
    
    def eval(self, env):
        if isinstance(self.left,Variable):
        
            if env.variables.get(self.left.getname(), None) is None:
                env.variables[self.left.getname()] = self.right.eval(env)
                return self.right.eval(env)
            
            # otherwise raise error
            raise ImmutableError(self.left.getname())
        
        else:
            raise LogicError("Cannot assign to this")
