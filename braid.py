#! /usr/bin/python
import sys
import repl, interpreter, parser
import os

def compile_file(filename):
    fd = os.open(filename,os.O_RDONLY,0777)
    contents = ''
    while True:
        buf = os.read(fd, 16)
        contents += buf
        if buf == '':
            # we're done
            break
    
    itpr = interpreter.Interpreter()
    contents = contents
    return itpr.compile_interpret(parser.parse(contents)).to_string()


def begin(args):
    if len(args) == 1:
        print args[0]
        print compile_file(args[0])
        
    elif len(args) == 0:
        repl.main()
    else:
        print "I don't understand these arguments"


if __name__ == '__main__':
    
    begin(sys.argv[1:])
