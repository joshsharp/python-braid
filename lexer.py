#from __future__ import unicode_literals
from rply import LexerGenerator
import re

lg = LexerGenerator()

# build up a set of token names and regexes they match
lg.add('FLOAT', '-?\d+\.\d+')
lg.add('INTEGER', '-?\d+')
lg.add('STRING', '(""".*?""")|(".*?")|(\'.*?\')')
lg.add('PRINT', 'print') # put this before variable which would otherwise match
lg.add('BOOLEAN', "true|false")
lg.add('IF', 'if')
lg.add('ELSE', 'else')
lg.add('END', 'end')
lg.add('AND', "and")
lg.add('OR', "or")
lg.add('NOT', "not")
lg.add('LET', 'let')
lg.add('FOR', 'for')
lg.add('WHILE', 'while')
lg.add('MATCH', 'match')
lg.add('ENUM', 'enum')
lg.add('NEW', 'new')
lg.add('RETURN', 'return')
lg.add('TYPE', 'type')
lg.add('TYPE_INTEGER', 'int')
lg.add('TYPE_STRING', 'str')
lg.add('TYPE_FLOAT', 'float')
lg.add('TYPE_CHAR', 'char')
lg.add('TYPE_LONG', 'long')
lg.add('TYPE_DOUBLE', 'double')
lg.add('RECORD', 'record')
lg.add('FUNCTION', 'func')
lg.add('LAMBDA', 'fn')
lg.add('PRIVATE', 'priv')
lg.add('MODULE', 'mod')
lg.add('TRAIT', 'trait')
lg.add('IMPLEMENT', 'impl')
lg.add('IMPORT', 'import')
lg.add('SEND', 'send')
lg.add('RECEIVE', 'receive')
lg.add('VARIABLE', "[a-zA-Z_][a-zA-Z0-9_]*")
lg.add('PLUS', '\+')
lg.add('==', '==')
lg.add('!=', '!=')
lg.add('>=', '>=')
lg.add('<=', '<=')
lg.add('>', '>')
lg.add('<', '<')
lg.add('=', '=')
lg.add('[', '\[')
lg.add(']', '\]')
lg.add('{', '\{')
lg.add('}', '\}')
lg.add('|', '\|')
lg.add(',', ',')
lg.add('DOT', '\.')
lg.add('COLON', ':')
lg.add('MINUS', '-')
lg.add('MUL', '\*')
lg.add('DIV', '/')
lg.add('MOD', '%')
lg.add('(', '\(')
lg.add(')', '\)')
lg.add('NEWLINE', '\n')

# ignore whitespace
lg.ignore('[ \t\r\f\v]+')

lexer = lg.build()

def lex(source):
    # explicitly remove comments
    comments = re.compile(r'#.*(\n|\Z)')
    source = comments.sub('\n',source)
    
    # remove multiple newlines
    multiline = re.compile(r'\n[\s]+')
    source = multiline.sub('\n',source)
    
    return lexer.lex(source)
