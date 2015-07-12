import lexer, parser, interpreter

def entry_point(argv):
    
    interpreter.loop()
    return 0

def target(*args):
    return entry_point, None
