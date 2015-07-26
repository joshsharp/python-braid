import lexer, parser, interpreter, repl

def entry_point(argv):
    
    repl.main()
    return 0

def target(*args):
    return entry_point, None
