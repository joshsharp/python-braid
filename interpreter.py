import parser, compiler, bytecode, objects

class Interpreter(object):

    def __init__(self):
        self.context = compiler.Context()
        self.variables = [objects.Null()] * 255

    def interpret(self, ast):
        byte_code = compiler.compile(ast, self.context)
        print byte_code.dump(True)
        
        pc = 0 # program counter
        stack = []
        
        while pc < len(byte_code.instructions):
            
            # the type of instruction
            opcode = byte_code.instructions[pc]
            # the optional arg
            arg = byte_code.instructions[pc + 1]
            # then increment
            pc += 2
            
            if opcode == bytecode.LOAD_CONST:
                # grab a value from our constants and add to stack
                value = byte_code.constants[arg]
                stack.append(value)
            
            elif opcode == bytecode.LOAD_VARIABLE:
                value = self.variables[arg]
                stack.append(value)
            
            elif opcode == bytecode.STORE_VARIABLE:
                value = stack.pop()
                self.variables[arg] = value
                stack.append(value)
            
            elif opcode == bytecode.PRINT:
                value = stack.pop()
                print value.to_string()
                stack.append(objects.Null())
            
            elif opcode == bytecode.BINARY_ADD:
                right = stack.pop()
                left = stack.pop()
                result = left.add(right)
                stack.append(result)
            
            elif opcode == bytecode.BINARY_SUB:
                right = stack.pop()
                left = stack.pop()
                result = left.sub(right)
                stack.append(result)
            
            elif opcode == bytecode.RETURN:
                if arg > 0:
                    if len(stack) > 0:
                        result = stack.pop()
                        return result
                    return objects.Null()
            
            elif opcode == bytecode.JUMP_IF_NOT_ZERO:
                val = stack.pop()
                if val.equals(objects.Boolean(True)):
                    pc = arg
                    
            elif opcode == bytecode.JUMP_IF_ZERO:
                val = stack.pop()
                if not val.equals(objects.Boolean(True)):
                    pc = arg

