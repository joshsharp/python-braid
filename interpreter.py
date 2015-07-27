import parser, compiler, bytecode, objects, errors

class Interpreter(object):

    def __init__(self):
        self.context = compiler.Context()
        
    def compile_interpret(self, ast):
        byte_code = compiler.compile(ast, self.context)
        print byte_code.dump(True)
    
        return self.interpret(byte_code)
    
    def interpret(self, byte_code, args=[]):
        
        pc = 0 # program counter
        stack = []
        
        assert(len(args) == len(byte_code.arguments))
        
        for arg, value in zip(byte_code.arguments,args):
            byte_code.variables[arg.name] = value
        
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
                value = byte_code.variables[arg]
                stack.append(value)
            
            elif opcode == bytecode.STORE_VARIABLE:
                value = stack.pop()
                byte_code.variables[arg] = value
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
            
            elif opcode == bytecode.BINARY_EQ:
                right = stack.pop()
                left = stack.pop()
                result = left.equals(right)
                stack.append(result)
            
            elif opcode == bytecode.BINARY_GT:
                right = stack.pop()
                left = stack.pop()
                result = left.gt(right)
                stack.append(result)
            
            elif opcode == bytecode.BINARY_GTE:
                right = stack.pop()
                left = stack.pop()
                result = left.gte(right)
                stack.append(result)
            
            elif opcode == bytecode.BINARY_LT:
                right = stack.pop()
                left = stack.pop()
                result = left.lt(right)
                stack.append(result)
            
            elif opcode == bytecode.BINARY_LTE:
                right = stack.pop()
                left = stack.pop()
                result = left.lte(right)
                stack.append(result)
            
            elif opcode == bytecode.RETURN:
                if arg == "1":
                    if len(stack) > 0:
                        result = stack.pop()
                        return result
                    return objects.Null()
            
            elif opcode == bytecode.JUMP_IF_NOT_ZERO:
                val = stack.pop()
                if val.equals(objects.Boolean(True)).value:
                    pc = arg
                    
            elif opcode == bytecode.JUMP_IF_ZERO:
                val = stack.pop()
                if not val.equals(objects.Boolean(True)).value:
                    pc = arg

            elif opcode == bytecode.JUMP:
                pc = arg

            elif opcode == bytecode.CALL:
                func = byte_code.constants[arg]
                args = []
                if len(func.arguments) > len(stack):
                    raise Exception("Not enough arguments")
                
                for i in range(0,len(func.arguments)):
                    args.append(stack.pop())
                stack.append(self.interpret(func,args))

        return stack[len(stack) - 1]
        

