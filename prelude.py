import os
import objects

def print_fn(args):
    
    print args[0].to_string()
    return objects.Null()


def readline(args):
    prompt = args[0]
    os.write(1,prompt.to_string())
        
    res = ''
    while True:
        buf = os.read(0, 16)
        if not buf:
            return objects.String(res)
        res += buf
        if res[-1] == '\n':
            #print res[:-1] == ""
            return objects.String(res[:-1])
