import lexer, parser, interpreter, repl, main

def entry_point(argv):
    main.begin(argv[1:])
    return 0

def target(*args):
    return entry_point, None
