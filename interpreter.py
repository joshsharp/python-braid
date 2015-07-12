import parser

if __name__ == '__main__':

    while True:
        # loop forever until KeyboardInterrupt or other break
        
        code = raw_input('>>> ')
        try:
            print "= %s" % parser.parse(code).eval()
        except ValueError as e:
            print "ERROR: " + e.message
            continue

