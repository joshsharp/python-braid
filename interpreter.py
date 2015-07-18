#from __future__ import unicode_literals
import parser
import sys, locale, os

class Environment(object):
    
    def __init__(self):
        self.variables = {}


env = Environment()
env.variables['VERSION'] = parser.String('0.0.1') # special value


def readline(prompt=None):
    
    if prompt:
        os.write(1,prompt)
        
    res = ''
    while True:
        buf = os.read(0, 16)
        if not buf: return res
        res += buf
        if res[-1] == '\n': return res


def printresult(result, prefix):
    #print type(result)
    print prefix + result.to_string()
   
def loop():
    state = parser.state
    last = parser.Null()
    
    opening = 0
    code = ''
    
    try:
        while True:
            
            # loop forever until KeyboardInterrupt or other break
            if opening > 0:
                code += readline('... ')
            else:                
                code = readline('>>> ') #.decode(sys.stdin.encoding or locale.getpreferredencoding(True) or 'ascii')
            if code.strip() == '':
                continue
            if code.strip() == ':a':
                print last.rep()
                continue
            if code.strip() == ':e':
                for key, var in env.variables.iteritems():
                    print str(key) + ': ' + var.to_string()
                continue
            if code.strip() == ':q':
                os.write(1, "\n")
                break
            
            try:
                ast = parser.parse(code, state) # at this point we get AST
                last = ast # store AST for later inspection
                result = ast.eval(env)
                env.variables['it'] = result
                printresult(result,"= ")
                opening = 0
            
            except parser.UnexpectedEndError as e:
                # just keep ignoring this till we break or complete
                opening += 1
                continue
            
            except parser.LogicError as e:
                opening = 0 # reset
                os.write(2, "ERROR: Cannot perform that operation\n")
                continue

            except parser.UnexpectedTokenError as e:
                opening = 0 # reset
                os.write(2, "ERROR: Unexpected '" + e.token + "'\n")
                continue

    except KeyboardInterrupt:
        os.write(1, "\n")


if __name__ == '__main__':
    os.write(1, "Interpreter v%s\n" % env.variables['VERSION'].to_string())
    loop()
