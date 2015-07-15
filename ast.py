from rply.token import BaseBox

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
    

class Noop(BaseBox):
    
    def eval(self, env):
        return self
    
    def to_string(self):
        return '(noop)'

    def rep(self):
        return 'Noop()'

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
        raise ValueError("Cannot compare that to boolean")
    
    def add(self, right):
        raise ValueError("Cannot add that to boolean")
    
    def sub(self, right):
        raise ValueError("Cannot sub that from boolean")
    
    def mul(self, right):
        raise ValueError("Cannot mul that to boolean")
    
    def div(self, right):
        raise ValueError("Cannot div that from boolean")
    
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
        raise ValueError("Cannot compare that to integer")
    
    def add(self, right):
    
        if type(right) is Integer:
            return Integer(self.value + right.value)
        if type(right) is Float:
            return Float(self.value + right.value)
        raise ValueError("Cannot add that to integer")
    
    def sub(self, right):
        if type(right) is Integer:
            return Integer(self.value - right.value)
        if type(right) is Float:
            return Float(self.value - right.value)
        raise ValueError("Cannot sub from int")
    
    def mul(self, right):
        if type(right) is Integer:
            return Integer(self.value * right.value)
        if type(right) is Float:
            return Float(self.value * right.value)
        raise ValueError("Cannot mul that to int")
    
    def div(self, right):
        if type(right) is Integer:
            return Integer(self.value / right.value)
        if type(right) is Float:
            return Float(self.value / right.value)
        raise ValueError("Cannot div that with int")

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
        raise ValueError("Cannot compare that to float")
    
    def add(self, right):
    
        if type(right) is Integer:
            return Float(self.value + right.value)
        if type(right) is Float:
            return Float(self.value + right.value)
        raise ValueError("Cannot add that to float")
    
    def sub(self, right):
        if type(right) is Float:
            return Float(self.value - right.value)
        if type(right) is Integer:
            return Float(self.value - right.value)
        raise ValueError("Cannot sub string")
    
    def mul(self, right):
        if type(right) is Integer:
            return Float(self.value * right.value)
        if type(right) is Float:
            return Float(self.value * right.value)
        raise ValueError("Cannot mul that to float")
    
    def div(self, right):
        if type(right) is Integer:
            return Float(self.value / right.value)
        if type(right) is Float:
            return Float(self.value / right.value)
        raise ValueError("Cannot div that with float")

    def rep(self):
        return 'Float(%s)' % self.value

class String(BaseBox):
    def __init__(self, value):
        self.value = str(value)

    def eval(self, env):
        return self

    def to_string(self):
        return str(self.value)

    def equals(self, right):
        if type(right) is String:
            return Boolean(self.value == right.value)
        if type(right) is Boolean:
            length = int(len(self.value) != 0)
            return Boolean(length == right.to_int())
        raise ValueError("Cannot compare that to string")
    
    def add(self, right):
    
        if type(right) is Integer:
            return String(self.value + str(right.value))
        if type(right) is Float:
            return String(self.value + str(right.value))
        if type(right) is String:
            return String(self.value + right.value)
        raise ValueError("Cannot add that to string")
    
    def sub(self, right):
        if type(right) is Integer:
            
            sli = len(self.value) - right.value
            assert(sli >= 0)
            return String(self.value[:sli])
        if type(right) is Float:
            
            sli = len(self.value) - int(right.value)
            assert(sli >= 0)
            return String(self.value[:sli])
        raise ValueError("Cannot sub string")
    
    def mul(self, right):
        if type(right) is Integer:
            return String(self.value * right.value)
        if type(right) is Float:
            return String(self.value * int(right.value))
        raise ValueError("Cannot multiply string with that")
    
    def div(self, right):
        raise ValueError("Cannot divide a string")
    
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
        raise ValueError("Not yet defined")
    
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
    def __init__(self, condition, body, else_body=None):
        self.condition = condition
        self.body = body
        self.else_body = else_body
        
    def eval(self, env):
        condition = self.condition.eval(env)
        if Boolean(True).equals(condition).value:
            
            return self.body.eval(env)
        else:
            
            if self.else_body is not None:
                return self.else_body.eval(env)
        return Noop()

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
        raise ValueError("Cannot modify value")
