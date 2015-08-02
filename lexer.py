#from __future__ import unicode_literals
from rply import LexerGenerator
try:
    import rpython.rlib.rsre.rsre_re as re
except:    
    import re

lg = LexerGenerator()

# build up a set of token names and regexes they match
lg.add('FLOAT', '-?\d+\.\d+')
lg.add('INTEGER', '-?\d+')
lg.add('STRING', '(""".*?""")|(".*?")|(\'.*?\')')
lg.add('PRINT', 'print(?!\w)') # put this before variable which would otherwise match
lg.add('BOOLEAN', "true(?!\w)|false(?!\w)")
lg.add('IF', 'if(?!\w)')
lg.add('ELSE', 'else(?!\w)')
lg.add('END', 'end(?!\w)')
lg.add('AND', "and(?!\w)")
lg.add('OR', "or(?!\w)")
lg.add('NOT', "not(?!\w)")
lg.add('LET', 'let(?!\w)')
lg.add('FOR', 'for(?!\w)')
lg.add('WHILE', 'while(?!\w)')
lg.add('BREAK', 'break(?!\w)')
lg.add('CONTINUE', 'continue(?!\w)')
lg.add('MATCH', 'match(?!\w)')
lg.add('ENUM', 'enum(?!\w)')
lg.add('NEW', 'new(?!\w)')
lg.add('RETURN', 'return(?!\w)')
lg.add('TYPE', 'type(?!\w)')
lg.add('TYPE_ARRAY', 'array(?!\w)')
lg.add('TYPE_DICT', 'dict(?!\w)')
lg.add('TYPE_INTEGER', 'int(?!\w)')
lg.add('TYPE_STRING', 'str(?!\w)')
lg.add('TYPE_FLOAT', 'float(?!\w)')
lg.add('TYPE_CHAR', 'char(?!\w)')
lg.add('TYPE_LONG', 'long(?!\w)')
lg.add('TYPE_DOUBLE', 'double(?!\w)')
lg.add('RECORD', 'record(?!\w)')
lg.add('FUNCTION', 'func(?!\w)')
lg.add('LAMBDA', 'fn(?!\w)')
lg.add('PRIVATE', 'priv(?!\w)')
lg.add('MODULE', 'mod(?!\w)')
lg.add('TRAIT', 'trait(?!\w)')
lg.add('IMPLEMENT', 'impl(?!\w)')
lg.add('IMPORT', 'import(?!\w)')
lg.add('SEND', 'send(?!\w)')
lg.add('RECEIVE', 'receive(?!\w)')
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

    comments = r'(#.*)(?:\n|\Z)'
    multiline = r'([\s]+)(?:\n)'
    
    comment = re.search(comments,source)
    while comment is not None:
        start, end = comment.span(1)
        assert start >= 0 and end >= 0
        source = source[0:start] + source[end:] #remove string part that was a comment
        comment = re.search(comments,source)

    line = re.search(multiline,source)
    while line is not None:
        start, end = line.span(1)
        assert start >= 0 and end >= 0
        source = source[0:start] + source[end:] #remove string part that was an empty line
        line = re.search(multiline,source)

    #print "source is now: %s" % source

    return lexer.lex(source)
