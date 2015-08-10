import lexer, parser, interpreter, repl, braid

def entry_point(argv):
    braid.begin(argv[1:])
    return 0

def target(*args):
    return entry_point, None
