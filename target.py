import lexer, parser, interpreter

def entry_point(argv):
    
    interpreter.main()
    return 0

def target(*args):
    return entry_point, None
