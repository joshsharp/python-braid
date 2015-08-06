import parser, compiler, interpreter, errors
import sys, locale, os


def readline(prompt=None):
    
    if prompt:
        os.write(1,prompt)
        
    res = ''
    while True:
        buf = os.read(0, 16)
        if not buf: return res
        res += buf
        if res[-1] == '\n': return res[:-1]


def printresult(result, prefix):
    #print type(result)
    if result is not None:
        print prefix + result.to_string()
    else:
        print prefix
def loop():
    intr = interpreter.Interpreter()
    context = compiler.Context()
    last = parser.Null()
    
    opening = 0
    code = ''
    
    try:
        while True:
            
            # loop forever until KeyboardInterrupt or other break
            if opening > 0:
                code += '\n' + readline('... ')
            else:                
                code = readline('>>> ') #.decode(sys.stdin.encoding or locale.getpreferredencoding(True) or 'ascii')
            if code.strip() == '':
                continue
            if code.strip() == ':a':
                print last.rep()
                continue
            if code.strip() == ':q':
                os.write(1, "\n")
                break
            
            try:
                ast = parser.parse(code) # at this point we get AST
                last = ast # store AST for later inspection
                #result = ast.eval(env)
                #env.variables['it'] = result
                
                result = intr.compile_interpret(ast, context)
                printresult(result,"= ")
                
                context.instructions = []
                opening = 0
            
            except parser.UnexpectedEndError as e:
                # just keep ignoring this till we break or complete
                opening += 1
                continue
            
            except parser.LogicError as e:
                opening = 0 # reset
                os.write(2, "ERROR: Cannot perform that operation (%s)\n" % e)
                continue
            
            except parser.ImmutableError as e:
                opening = 0 # reset
                os.write(2, "ERROR: Cannot reassign that (%s)\n" % e)
                continue
            
            except parser.UnexpectedTokenError as e:
                opening = 0 # reset
                os.write(2, "ERROR: Unexpected '" + e.token + "'\n")
                continue
            
            except Exception as e:
                opening = 0 # reset
                os.write(2, "ERROR: %s\n" % (str(e)))
                continue

    except KeyboardInterrupt:
        os.write(1, "\n")

def main():
    os.write(1, "Mtn interpreter\n")
    loop()

if __name__ == '__main__':
    main()
