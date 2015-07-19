#from __future__ import unicode_literals
from rply import ParserGenerator
from rply.token import BaseBox, Token
from ast import *
from errors import *
import lexer
import os

# state instance which gets passed to parser
class ParserState(object):
    def __init__(self):
        # we want to hold a dict of declared variables
        self.variables = {}

pg = ParserGenerator(
    # A list of all token names, accepted by the parser.
    ['PRINT', 'STRING', 'INTEGER', 'FLOAT', 'VARIABLE', 'BOOLEAN',
     'PLUS', 'MINUS', 'MUL', 'DIV',
     'IF', 'ELSE', 'COLON', 'END', 'AND', 'OR', 'NOT',
     '(', ')', '=', '==', '!=', '>=', '<=', '<', '>', '[', ']', ',',
     '$end', 'NEWLINE', 'COMMENT',
     
    ],
    # A list of precedence rules with ascending precedence, to
    # disambiguate ambiguous production rules.
    precedence=[
        ('left', ['=']),
        ('left', ['[',']',',']),
        ('left', ['IF', 'COLON', 'ELSE', 'END', 'NEWLINE','COMMENT']),
        ('left', ['AND', 'OR',]),
        ('left', ['NOT',]),
        ('left', ['==', '!=', '>=','>', '<', '<=',]),
        ('left', ['PLUS', 'MINUS',]),
        ('left', ['MUL', 'DIV',]),
        
    ]
)

@pg.production("main : program")
def main_program(self, p):
    return p[0]

@pg.production('program : statement_full')
def program_statement(state, p):
    return Program(p[0])

@pg.production('program : statement_full program')
def program_statement_program(state, p):
    if type(p[1]) is Program:
        program = p[1]
    else:
        program = Program(p[12])
    
    program.add_statement(p[0])
    return p[1]

@pg.production('block : statement_full')
def block_expr(state, p):
    return Block(p[0])


@pg.production('block : statement_full block')
def block_expr_block(state, p):
    if type(p[1]) is Block:
        b = p[1]
    else:
        b = Block(p[1])
    
    b.add_statement(p[0])
    return b


#@pg.production('statement_full : comment_line')
@pg.production('statement_full : statement COMMENT')
@pg.production('statement_full : statement COMMENT NEWLINE')
@pg.production('statement_full : statement NEWLINE')
@pg.production('statement_full : statement NEWLINE COMMENT NEWLINE')
@pg.production('statement_full : statement NEWLINE COMMENT $end')
@pg.production('statement_full : statement NEWLINE COMMENT')
@pg.production('statement_full : statement $end')
def statement_full(state, p):
    return p[0]

@pg.production('statement : expression')
def statement_expr(state, p):
    return p[0]

@pg.production('expression : PRINT ( expression )')
def statement_print(state, p):    
    #os.write(1, p[2].eval())
    return Print(p[2])

@pg.production('statement : VARIABLE = expression')
def statement_assignment(state, p):
    return Assignment(Variable(p[0].getstr()),p[2])

@pg.production('const : FLOAT')
def expression_float(state, p):
    # p is a list of the pieces matched by the right hand side of the rule
    return Float(float(p[0].getstr()))

@pg.production('const : BOOLEAN')
def expression_boolean(state, p):
    # p is a list of the pieces matched by the right hand side of the rule
    return Boolean(True if p[0].getstr() == 'true' else False)

@pg.production('const : INTEGER')
def expression_integer(state, p):
    return Integer(int(p[0].getstr()))

@pg.production('const : STRING')
def expression_string(state, p):
    return String(p[0].getstr().strip('"\''))

@pg.production('expression : const')
def expression_const(state, p):
    return p[0]

@pg.production('expressionlist : expression')
def expressionlist_single(state, p):
    return p[0]

@pg.production('expressionlist : expression , expressionlist')
def expressionlist(state, p):
    b = Array(p[2])
    b.push(p[0])
    return b

@pg.production('expression : [ expressionlist ]')
def expression_array(state, p):
    return p[1]

@pg.production('expression : IF expression COLON statement END')
def expression_if_single_line(state, p):
    return If(condition=p[1],body=p[3])

@pg.production('expression : IF expression COLON statement ELSE COLON statement END')
def expression_if_else_single_line(state, p):
    return If(condition=p[1],body=p[3],else_body=p[6])

@pg.production('expression : IF expression COLON COMMENT block END')
@pg.production('expression : IF expression COLON NEWLINE block END')
def expression_if(state, p):
    return If(condition=p[1],body=p[4])

@pg.production('expression : IF expression COLON COMMENT block ELSE COLON COMMENT block END')
@pg.production('expression : IF expression COLON COMMENT block ELSE COLON NEWLINE block END')
@pg.production('expression : IF expression COLON NEWLINE block ELSE COLON COMMENT block END')
@pg.production('expression : IF expression COLON NEWLINE block ELSE COLON NEWLINE block END')
def expression_if_else(state, p):
    return If(condition=p[1],body=p[4],else_body=p[8])

@pg.production('expression : VARIABLE')
def expression_variable(state, p):
    # cannot return the value of a variable if it isn't yet defined
    return Variable(p[0].getstr())

@pg.production('expression : NOT expression ')
def expression_not(state, p):
    return Not(p[1])

@pg.production('expression : ( expression )')
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
        raise LogicError('Oops, this should not be possible!')

@pg.production('expression : expression != expression')
@pg.production('expression : expression == expression')
@pg.production('expression : expression >= expression')
@pg.production('expression : expression <= expression')
@pg.production('expression : expression > expression')
@pg.production('expression : expression < expression')
@pg.production('expression : expression AND expression')
@pg.production('expression : expression OR expression')
def expression_equality(state, p):
    left = p[0]
    right = p[2]
    check = p[1]
    
    if check.gettokentype() == '==':
        return Equal(left, right)
    elif check.gettokentype() == '!=':
        return NotEqual(left, right)
    elif check.gettokentype() == '>=':
        return GreaterThanEqual(left, right)
    elif check.gettokentype() == '<=':
        return LessThanEqual(left, right)
    elif check.gettokentype() == '>':
        return GreaterThan(left, right)
    elif check.gettokentype() == '<':
        return LessThan(left, right)
    elif check.gettokentype() == 'AND':
        return And(left, right)
    elif check.gettokentype() == 'OR':
        return Or(left, right)
    else:
        raise LogicError("Shouldn't be possible")

@pg.error
def error_handler(state, token):
    # we print our state for debugging porpoises
    #print token
    pos = token.getsourcepos()
    if pos:
        raise UnexpectedTokenError(token.gettokentype())
    elif token.gettokentype() == '$end':
        raise UnexpectedEndError()
    else:
        raise UnexpectedTokenError(token.gettokentype())

parser = pg.build()
state = ParserState()

def parse(code, state):
    
    result = parser.parse(lexer.lex(code),state)
    return result

