import parser, compiler, interpreter, errors, objects
import sys, locale, os


def readline(prompt=None):
    
    if prompt:
        os.write(1,prompt)
        
    res = ''
    while True:
        buf = os.read(0, 16)
        if not buf:
            return res
        res += buf
        if res[-1] == '\n':
            return res[:-1]

def printresult(result, prefix):
    #print type(result)
    if result is not None:
        print "%s %s" % (prefix, result.to_string())
    else:
        print prefix

def loop():
    intr = interpreter.Interpreter()
    #context = compiler.Context()
    last = parser.Null()
    bytecode = ''
    
    opening = 0
    code = ''
    
    try:
        while True:
            
            # loop forever until KeyboardInterrupt or other break
            if opening > 0:
                code += '\n' + readline('... ')
            else:                
                code = readline('>>> ')
            if code.strip(' \t\r\n') == '':
                continue
            if code.strip(' \t\r\n') == ':a':
                print last.rep()
                continue
            if code.strip(' \t\r\n') == ':b':
                print bytecode
                continue
            if code.strip(' \t\r\n') == ':q':
                os.write(1, "\n")
                break
            
            try:
                ast = parser.parse(code) # at this point we get AST
                last = ast # store AST for later inspection
                #result = ast.eval(env)
                #env.variables['it'] = result
                
                result = intr.compile_interpret(ast)
                bytecode = intr.last_bc
                printresult(result,"= ")
                
                #context.instructions = []
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
                os.write(2, "ERROR: Unexpected '%s'\n" % e.token)
                continue
            
            except Exception as e:
                opening = 0 # reset
                os.write(2, "ERROR: %s %s\n" % (e.__class__.__name__, str(e)))
                continue

    except KeyboardInterrupt:
        os.write(1, "\n")

def main():
    os.write(1, "Braid interpreter\n")
    loop()

if __name__ == '__main__':
    main()
