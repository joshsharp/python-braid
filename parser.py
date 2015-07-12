#from __future__ import unicode_literals
from rply import ParserGenerator
from rply.token import BaseBox
import lexer
import os

# state instance which gets passed to parser
class ParserState(object):
    def __init__(self):
        # we want to hold a dict of declared variables
        self.variables = {}

# all token types inherit rply's basebox as rpython needs this
# these classes represent our Abstract Syntax Tree
class Integer(BaseBox):
    def __init__(self, value):
        self.value = int(value)

    def eval(self):
        return self
    
    def to_string(self):
        return str(self.value)
    
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
        return str(self.value)
    
    def add(self, right):
        return self.value.eval().add(right)
    
    def sub(self, right):
        return self.value.eval().sub(right)
    
    def mul(self, right):
        return self.value.eval().mul(right)
    
    def div(self, right):
        return self.value.eval().div(right)


class BinaryOp(BaseBox):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    
    def to_string(self):
        return str(self.eval())


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


pg = ParserGenerator(
    # A list of all token names, accepted by the parser.
    ['PRINT', 'STRING', 'INTEGER', 'FLOAT', 'VARIABLE',
     'OPEN_PARENS', 'CLOSE_PARENS',
     'PLUS', 'MINUS', 'MUL', 'DIV', 'EQUALS', 
    ],
    # A list of precedence rules with ascending precedence, to
    # disambiguate ambiguous production rules.
    precedence=[
        ('left', ['PLUS', 'MINUS']),
        ('left', ['MUL', 'DIV'])
    ]
)

# this decorator defines the grammar to be matched and passed in as 'p'
@pg.production('statement : PRINT OPEN_PARENS expression CLOSE_PARENS')
def statement_print(state, p):
    
    #os.write(1, p[2].eval())
    printresult(p[2],'')
    return p[2]

@pg.production('statement : VARIABLE EQUALS expression')
def statement_assignment(state, p):
    # only assign value if variable is not yet defined - immutable values
    if state.variables.get(p[0].getstr(), None) is None:
        state.variables[p[0].getstr()] = p[2]
        return p[2]
    
    # otherwise raise error
    raise ValueError("Cannot modify value")
    

@pg.production('statement : expression')
def statement_expr(state, p):
    return p[0]

@pg.production('const : FLOAT')
def expression_float(state, p):
    # p is a list of the pieces matched by the right hand side of the rule
    return Float(float(p[0].getstr()))

@pg.production('const : INTEGER')
def expression_integer(state, p):
    return Integer(int(p[0].getstr()))

@pg.production('const : STRING')
def expression_string(state, p):
    return String(p[0].getstr().strip('"\''))

@pg.production('expression : const')
def expression_const(state, p):
    return p[0]

@pg.production('expression : VARIABLE')
def expression_variable(state, p):
    # cannot return the value of a variable if it isn't yet defined
    if state.variables.get(p[0].getstr(), None) is None:
        raise ValueError("Not yet defined")
    # otherwise return value from state
    return state.variables[str(p[0].getstr())]

@pg.production('expression : OPEN_PARENS expression CLOSE_PARENS')
def expression_parens(state, p):
    # in this case we need parens only for precedence
    # so we just need to return the inner expression
    return p[1]

@pg.production('expression : expression PLUS expression')
@pg.production('expression : expression MINUS expression')
@pg.production('expression : expression MUL expression')
@pg.production('expression : expression DIV expression')
def expression_binop(state, p):
    left = p[0]
    right = p[2]
    
    if p[1].gettokentype() == 'PLUS':
        return Add(left, right)
    elif p[1].gettokentype() == 'MINUS':
        return Sub(left, right)
    elif p[1].gettokentype() == 'MUL':
        return Mul(left, right)
    elif p[1].gettokentype() == 'DIV':
        return Div(left, right)
    else:
        raise AssertionError('Oops, this should not be possible!')

@pg.error
def error_handler(state, token):
    # we print our state for debugging porpoises
    print token
    raise ValueError("Unexpected %s at %s" % (token.gettokentype(), token.getsourcepos()))

parser = pg.build()
state = ParserState()
state.variables['__version__'] = String('0.0.0') # special value under '__version__'

def parse(code):
    return parser.parse(lexer.lex(code),state)

def printresult(result, prefix):
    
    print prefix + result.eval().to_string()