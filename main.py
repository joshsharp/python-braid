import sys
import repl, interpreter, parser
import os

def compile_file(filename):
    fd = os.open(args[0],os.O_RDONLY)
    contents = ''
    while True:
        buf = os.read(fd, 16)
        contents += buf
        if buf == '':
            # we're done
            break
    
    itpr = interpreter.Interpreter()
    return itpr.compile_interpret(parser.parse(contents)).to_string()
    

if __name__ == '__main__':
    
    args = sys.argv[1:]
    if len(args) == 1:
        print args[0]
        print compile_file(args[0])
        
    elif len(args) == 0:
        repl.main()
    else:
        print "I don't understand these arguments"

        
