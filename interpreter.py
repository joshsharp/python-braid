import parser, compiler, bytecode, objects, errors

class Interpreter(object):

    def __init__(self):
        self.context = compiler.Context()
        
    def compile_interpret(self, ast):
        byte_code = compiler.compile(ast, self.context)
        #print byte_code.dump(True)
    
        return self.interpret(byte_code)
    
    def interpret(self, byte_code, args=[]):
        
        pc = 0 # program counter
        stack = []
        variables = [objects.Null()] * 255
        
        assert(len(args) == len(byte_code.arguments))
        
        #for index, value in zip(byte_code.arguments,args):
        #    byte_code.variables[index] = value
        
        print "(running %s)" % byte_code.name
        
        for i in xrange(0,len(args)):
            index = byte_code.arguments[i]
            print "(arg %s going into %s)" % (args[i].dump(),index)
            byte_code.variables[index] = objects.Variable("arg",args[i])
        
        while pc < len(byte_code.instructions):
            
            # the type of instruction and arg (a tuple)
            opcode, arg = byte_code.instructions[pc]
            
            print "(%s %s %s)" % (pc, bytecode.reverse[opcode], arg)
            
            # then increment
            pc += 1
            
            if opcode == bytecode.LOAD_CONST:
                # grab a value from our constants and add to stack
                value = byte_code.constants[arg]
                stack.append(value)
            
            elif opcode == bytecode.LOAD_VARIABLE:
                var = byte_code.variables[arg]
                assert(isinstance(var,objects.Variable))
                #print "- appending value %s" % var.value.dump()
                stack.append(var.value)
            
            elif opcode == bytecode.STORE_VARIABLE:
                value = stack.pop()
                oldvar = byte_code.variables[arg]
                assert(isinstance(oldvar,objects.Variable))
                byte_code.variables[arg] = objects.Variable(oldvar.name,value)
                stack.append(value)
            
            elif opcode == bytecode.STORE_ARRAY:
                values = []
                for i in xrange(arg):
                    values.append(stack.pop())
                stack.append(objects.Array(values))
            
            elif opcode == bytecode.PRINT:
                value = stack.pop()
                print value.to_string()
                stack.append(objects.Null())
            
            elif opcode == bytecode.INDEX:
                left = stack.pop()
                right = stack.pop()
                result = left.index(right)
                stack.append(result)
            
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
            
            elif opcode == bytecode.BINARY_MUL:
                right = stack.pop()
                left = stack.pop()
                result = left.mul(right)
                stack.append(result)
                
            elif opcode == bytecode.BINARY_DIV:
                right = stack.pop()
                left = stack.pop()
                result = left.div(right)
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
                if arg == 1:
                    if len(stack) > 0:
                        result = stack.pop()
                        return result
                    return objects.Null()
            
            elif opcode == bytecode.JUMP_IF_NOT_ZERO:
                val = stack.pop()
                assert(isinstance(val,objects.BaseBox))
                
                result = val.equals(objects.Boolean(True))
                assert(isinstance(result,objects.Boolean))
                if result.value:
                    pc = arg
                    
            elif opcode == bytecode.JUMP_IF_ZERO:
                val = stack.pop()
                assert(isinstance(val,objects.BaseBox))
                result = val.equals(objects.Boolean(True))
                assert(isinstance(result,objects.Boolean))
                if not result.value:
                    pc = arg

            elif opcode == bytecode.JUMP:
                pc = arg

            elif opcode == bytecode.CALL:
                func = byte_code.functions[arg]
                args = []
                if len(func.arguments) > len(stack):
                    raise Exception("Not enough arguments")
                
                for i in range(0,len(func.arguments)):
                    args.append(stack.pop())
                stack.append(self.interpret(func,args))

        return stack[len(stack) - 1]
        

