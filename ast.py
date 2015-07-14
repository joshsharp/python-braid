from rply.token import BaseBox

# all token types inherit rply's basebox as rpython needs this
# these classes represent our Abstract Syntax Tree
class Program(BaseBox):
    
    def __init__(self, statement):
        self.statements = []
        self.statements.append(statement)
    
    def add_statement(self, statement):
        self.statements.insert(0,statement)
        
    def eval(self):
        #print "count: %s" % len(self.statements)
        result = None
        for statement in self.statements:
            result = statement.eval()
            #print result.to_string()
        return result        

class Noop(BaseBox):
    
    def eval(self):
        return self
    
    def to_string(self):
        return '(noop)'

class Boolean(BaseBox):
    def __init__(self, value):
        self.value = bool(value)

    def eval(self):
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

class Integer(BaseBox):
    def __init__(self, value):
        self.value = int(value)

    def eval(self):
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


class Float(BaseBox):
    def __init__(self, value):
        self.value = float(value)

    def eval(self):
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


class String(BaseBox):
    def __init__(self, value):
        self.value = str(value)

    def eval(self):
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
    
    
class Variable(BaseBox):
    def __init__(self, value):
        self.value = value

    def eval(self):
        return self.value.eval()
    
    def to_string(self):
        return str(self.value.eval())
    
    def equals(self, right):
        return self.value.eval().equals(right)
    
    def add(self, right):
        return self.value.eval().add(right)
    
    def sub(self, right):
        return self.value.eval().sub(right)
    
    def mul(self, right):
        return self.value.eval().mul(right)
    
    def div(self, right):
        return self.value.eval().div(right)


class Print(BaseBox):
    def __init__(self, value):
        self.value = value
    
    def eval(self):
        print self.value.eval().to_string() + '\n'
        return self.value.eval() 
    
    def to_string(self):
        return self.value.eval().to_string()


class If(BaseBox):
    def __init__(self, condition, body, else_body=None):
        self.condition = condition
        self.body = body
        self.else_body = else_body
        
    def eval(self):
        condition = self.condition.eval()
        if Boolean(True).equals(condition).value:
            
            return self.body.eval()
        else:
            
            if self.else_body is not None:
                return self.else_body.eval()
        return Noop()

class BinaryOp(BaseBox):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    
    def to_string(self):
        return str(self.eval())

class Equal(BinaryOp):
    
    def eval(self):
        return self.left.eval().equals(self.right.eval())


class NotEqual(BinaryOp):
    
    def eval(self):
        result = self.left.eval().equals(self.right.eval())
        result.value = not result.value
        return result


class Add(BinaryOp):
    def eval(self):
        # this needs to call 'add' or something on the left, passing in the right
        # cannot check that types are 'primitives' eg. Float like we were doing
        # because compound expression like 5 + 5 + 5 will end up with
        # Add(Float,Add(Float)) tree.
        
        return self.left.eval().add(self.right.eval())
        
class Sub(BinaryOp):
    def eval(self):
        return self.left.eval().sub(self.right.eval())
        
        
class Mul(BinaryOp):
    def eval(self):
        return self.left.eval().mul(self.right.eval())
        
class Div(BinaryOp):
    def eval(self):
        return self.left.eval().div(self.right.eval())
