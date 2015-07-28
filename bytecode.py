
LOAD_CONST          = 1
BINARY_NEQ          = 2
PRINT               = 3
BINARY_EQ           = 4
RETURN              = 5
STORE_VARIABLE      = 6
LOAD_VARIABLE       = 7

JUMP                = 8
JUMP_IF_NOT_ZERO    = 9
JUMP_IF_ZERO        = 10

BINARY_ADD          = 11
BINARY_SUB          = 12
BINARY_LT           = 13
BINARY_LTE          = 14
BINARY_GT           = 15
BINARY_GTE          = 16
BINARY_AND          = 17
BINARY_OR           = 18
NOT                 = 19
BINARY_MUL          = 20
BINARY_DIV          = 21
INDEX               = 50
CALL                = 90

NO_ARG              = -255


class Bytecode(object):
    """Also plundered from Cycy"""
    
    def __init__(self, instructions, arguments, constants, variables, functions, name):
        self.instructions = instructions
        self.name = name
        self.arguments = arguments or []
        self.constants = constants
        self.variables = variables
        self.functions = functions

    def __iter__(self):
        """Yield (offset, byte_code, arg) tuples.
        The `byte_code` will be one of the constants defined above,
        and `arg` may be None. `byte_code` and `arg` will be ints.
        """
        offset = 0
        while offset < len(self.instructions):
            byte_code, arg = self.instructions[offset]
            
            yield (offset, byte_code, arg)
            offset += 1

    def to_string(self):
        return 'bytecode'

    def dump(self, pretty=True, indent=0):
        for i, v in enumerate(self.constants):
            print "%s: %s" % (i, v.to_string())
        
        for k, v in self.variables.iteritems():
            print "%s: %s" % (k, v)
        
        
        lines = []

        for offset, byte_code, arg in self:

            name = byte_code

            str_arg = ""
            if arg != NO_ARG:
                str_arg = "%s" % arg

            line = "%s%s %s %s" % (' ' * indent, str(offset), name, str_arg)
            if pretty:
                if byte_code == LOAD_CONST:
                    line += " => " + self.constants[arg].dump()
                elif byte_code == CALL:
                    line += " => \n" + self.functions[arg].dump(True, indent=indent+2)
                        
                elif byte_code == RETURN:
                    if arg:
                        line += " (top of stack)"
                    else:
                        line += " (void return)"
            lines.append(line.strip())

        return "\n".join(lines)

