from rply import LexerGenerator

lg = LexerGenerator()

lg.add('FLOAT', '-?\d+\.\d+')
lg.add('INTEGER', '-?\d+')
lg.add('PRINT', 'print') # put this before variable which would otherwise match
lg.add('VARIABLE', "[a-zA-Z_][a-zA-Z0-9_]*")
lg.add('PLUS', '\+')
lg.add('EQUALS', '=')
lg.add('MINUS', '-')
lg.add('MUL', '\*')
lg.add('DIV', '/')
lg.add('OPEN_PARENS', '\(')
lg.add('CLOSE_PARENS', '\)')

lg.ignore('\s+')

lexer = lg.build()

def lex(source):
    return lexer.lex(source)