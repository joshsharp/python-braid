#from __future__ import unicode_literals
import parser
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

   
def loop():
    state = parser.state
    try:
        while True:
            # loop forever until KeyboardInterrupt or other break
            
            code = readline('>>> ') #.decode(sys.stdin.encoding or locale.getpreferredencoding(True) or 'ascii')
            if code.strip() == '':
                continue
            try:
                result = parser.parse(code, state)
                parser.state.variables['it'] = result
                parser.printresult(result,"= ")
            except ValueError as e:
                os.write(2, "ERROR: " + str(e) + "\n")
                continue

    except KeyboardInterrupt:
        os.write(1, "\n")
        exit()

if __name__ == '__main__':
    os.write(1, "Interpreter v%s\n" % parser.state.variables['VERSION'].to_string())
    loop()
