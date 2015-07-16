#from __future__ import unicode_literals
from rply import LexerGenerator

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
lg.add('VARIABLE', "[a-zA-Z_][a-zA-Z0-9_]*")
lg.add('PLUS', '\+')
lg.add('==', '={2}')
lg.add('!=', '!=')
lg.add('>=', '>=')
lg.add('<=', '<=')
lg.add('>', '>')
lg.add('<', '<')
lg.add('=', '=')
lg.add('[', '\[')
lg.add(']', '\]')
lg.add(',', ',')
lg.add('COLON', ':')
lg.add('MINUS', '-')
lg.add('MUL', '\*')
lg.add('DIV', '/')
lg.add('(', '\(')
lg.add(')', '\)')
lg.add('NEWLINE', '\n')

# ignore whitespace
lg.ignore('[ \t\r\f\v]+')
# ignore comments
lg.ignore(r'#.*(?:\n|\r|\r\n|\n\r|$)')

lexer = lg.build()

def lex(source):
    return lexer.lex(source)
