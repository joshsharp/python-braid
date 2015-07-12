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
    try:
        while True:
            # loop forever until KeyboardInterrupt or other break
            
            code = readline('>>> ') #.decode(sys.stdin.encoding or locale.getpreferredencoding(True) or 'ascii')
            try:
                result = parser.parse(code)
                parser.state.variables['it'] = result
                parser.printresult(result,"= ")
            except ValueError as e:
                print "ERROR: " + str(e)
                continue

    except KeyboardInterrupt:
        pass

if __name__ == '__main__':

    loop()
