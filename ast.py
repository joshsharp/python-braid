
from rply.token import BaseBox
from errors import *

# all token types inherit rply's basebox as rpython needs this
# these classes represent our Abstract Syntax Tree
# TODO: deprecate eval() as we move to compiling and then interpreting

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
            result += '\n\t' + statement.rep()
        result += '\n)'
        return result
    
    def get_statements(self):
        return self.statements


class FunctionDeclaration(BaseBox):
    
    def __init__(self, name, args, block):
        self.name = name
        self.args = args
        self.block = block
        
    def eval(self, env):
        raise LogicError("Cannot assign to this")
    
    def rep(self):
        result = 'FunctionDeclaration %s (' % self.name
        if isinstance(self.args,Array):
            for statement in self.args.get_statements():
                result += ' ' + statement.rep()
        result += ')'
        result += '\n\t('
        if isinstance(self.args,Block):
            for statement in self.block.get_statements():
                result += '\n\t' + statement.rep()
        result += '\n)'
        return result
    
    def to_string(self):
        return "<function '%s'>" % self.name


class Function(BaseBox):
    
    def __init__(self, name, args):
        self.name = name
        self.args = args
        
    def eval(self, env):
        result = Null()
        return result
    
    def rep(self):
        result = 'Function %s (' % self.name
        if isinstance(self.args,Array):
            for statement in self.args.get_statements():
                result += ' ' + statement.rep()
        result += ')'
        return result
    
    def to_string(self):
        return "<function '%s'>" % self.name


class Block(BaseBox):
    
    def __init__(self, statement):
        self.statements = []
        self.statements.append(statement)
    
    def add_statement(self, statement):
        self.statements.insert(0,statement)
    
    def get_statements(self):
        return self.statements
    
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
            result += '\n\t' + statement.rep()
        result += '\n)'
        return result


class InnerArray(BaseBox):
    """
    Only used to handle array values which are passed to Array.
    """
    
    def __init__(self, statements = None):
        self.statements = []
        self.values = []
        if statements:
            self.statements = statements

    def push(self, statement):
        self.statements.insert(0,statement)
    
    def append(self, statement):
        self.statements.append(statement)

    def extend(self, statements):
        self.statements.extend(statements)

    def get_statements(self):
        return self.statements


class Array(BaseBox):
    
    def map(self, fun, ls):  
        nls = []
        for l in ls:
          nls.append(fun(l))
        return nls
    
    def __init__(self, inner):
        self.statements = inner.get_statements()
        self.values = []
    
    def get_statements(self):
        return self.statements
    
    def push(self, statement):
        self.statements.insert(0,statement)
    
    def append(self, statement):
        self.statements.append(statement)
    
    def index(self, i):
        if type(i) is Integer:
            return self.values[i.value]
        if type(i) is Float:
            return self.values[int(i.value)]
        raise LogicError("Cannot index with that value")
    
    def add(self, right):
    
        if type(right) is Array:
            result = Array(InnerArray())
            result.values.extend(self.values)
            result.values.extend(right.values)
            return result
        raise LogicError("Cannot add that to array")
    
    def eval(self, env):
        
        if len(self.values) == 0:            
            for statement in self.statements:
                self.values.append(statement.eval(env))
        return self
    
    def rep(self):
        result = 'Array('
        result += ",".join(self.map(lambda x: x.rep(),self.statements))
        result += ')'
        return result
    
    def to_string(self):
        return '[%s]' % (", ".join(self.map(lambda x: x.to_string(),self.values)))


class InnerDict(BaseBox):
    """
    Only used to handle array values which are passed to Array.
    """
    
    def __init__(self, statements = None):
        self.data = {}
        self.values = {}
        if statements:
            self.data = statements

    def update(self, key, val):
        self.data[key] = val
    
    def get_data(self):
        return self.data


class Dict(BaseBox):
    
    def map(self, fun, ls):  
        nls = []
        for l in ls:
          nls.append(fun(l))
        return nls
    
    def __init__(self, inner):
        self.data = inner.get_data()
        self.values = {}
    
    def get_data(self):
        return self.data
    
    def update(self, key, val):
        self.data[key] = val
    
    def eval(self, env):
        
        if len(self.values) == 0:            
            for statement in self.statements:
                self.values.append(statement.eval(env))
        return self
    
    def rep(self):
        result = 'Dict('
        result += ",".join(self.map(lambda k: "%s: %s" % (k[0].rep(), k[1].rep()),self.data.iteritems()))
        result += ')'
        return result
    
    def to_string(self):
        return '{ %s }' % (", ".join(self.map(lambda k: "%s: %s" % (k[0].to_string(), k[1].to_string()),self.values.iteritems())))


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
    
    def rep(self):
        return 'Boolean(%s)' % self.value


class Integer(BaseBox):
    def __init__(self, value):
        self.value = int(value)

    def eval(self, env):
        return self
    
    def to_string(self):
        return str(self.value)
    
    def rep(self):
        return 'Integer(%s)' % self.value


class Float(BaseBox):
    def __init__(self, value):
        self.value = float(value)

    def eval(self, env):
        return self

    def to_string(self):
        return str(self.value)

    def rep(self):
        return 'Float(%s)' % self.value


class String(BaseBox):
    def __init__(self, value):
        self.value = str(value)

    def eval(self, env):
        return self

    def to_string(self):
        return '"%s"' % str(self.value)

    def rep(self):
        return 'String("%s")' % self.value
        
    
class Variable(BaseBox):
    def __init__(self, name):
        self.name = str(name)
        self.value = None

    def getname(self):
        return str(self.name)

    def eval(self, env):
        if env.variables.get(self.name, None) is not None:
            self.value = env.variables[self.name].eval(env)
            return self.value
        raise LogicError("Not yet defined")
    
    def to_string(self):
        return str(self.name)
    
    def rep(self):
        return 'Variable(%s)' % self.name
        

class Print(BaseBox):
    def __init__(self, value):
        self.value = value
    
    def eval(self, env):
        print self.value.eval(env).to_string()
        return Null() #self.value.eval(env) 
    
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


class While(BaseBox):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body
        
    def eval(self, env):
        return Null()

    def rep(self):
        return 'While(%s) Then(%s)' % (self.condition.rep(), self.body.rep())


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


class And(BinaryOp):
    
    def rep(self):
        return 'And(%s, %s)' % (self.left.rep(), self.right.rep())
    
    def eval(self, env):
        one = self.left.eval(env).equals(Boolean(True))
        two = self.right.eval(env).equals(Boolean(True))
        return Boolean(one.value and two.value)


class Or(BinaryOp):
    
    def rep(self):
        return 'Or(%s, %s)' % (self.left.rep(), self.right.rep())
    
    def eval(self, env):
        one = self.left.eval(env).equals(Boolean(True))
        two = self.right.eval(env).equals(Boolean(True))
        # must remember to use inner primitive values
        return Boolean(one.value or two.value)


class Not(BaseBox):
    
    def __init__(self, value):
        self.value = value
    
    def rep(self):
        return 'Not(%s)' % (self.value.rep())
    
    def eval(self, env):
        result = self.value.eval(env)
        if isinstance(result,Boolean):
            return Boolean(not result.value)
        raise LogicError("Cannot 'not' that")


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
                env.variables[self.left.getname()] = self.right
                return self.right.eval(env)
            
            # otherwise raise error
            raise ImmutableError(self.left.getname())
        
        else:
            raise LogicError("Cannot assign to this")


class Index(BinaryOp):
    
    def rep(self):
        return  'Index(%s, %s)' % (self.left.rep(), self.right.rep())
    
    def eval(self, env):
        
        left = self.left.eval(env)
        if type(left) is Array:
            return left.index(self.right.eval(env))
        if type(left) is String:
            return left.index(self.right.eval(env))
        
        raise LogicError("Cannot index this")
