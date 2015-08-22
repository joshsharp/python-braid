import parser, compiler, bytecode, objects, errors, prelude

class Interpreter(object):

    def __init__(self):
        self.last_bc = ''
        self.context = compiler.Context()
        self.import_prelude()
    
    def import_prelude(self):
        index = self.context.register_variable("print")
        self.context.variables[index] = objects.Variable("print",objects.ExternalFunction("print",prelude.print_fn,1))
        
        index = self.context.register_variable("readline")
        self.context.variables[index] = objects.Variable("readline",objects.ExternalFunction("readline",prelude.readline,1))
        
        
    def compile_interpret(self, ast, context=None):
        if not context:
            context = self.context
        byte_code = compiler.compile(ast, context)
        self.last_bc = ''
    
        return self.interpret(byte_code)
    
    def copy_context(self, code_from, code_to):
        for k, v in code_from.variables.iteritems():
            code_to.variables[k] = v
    
    def interpret(self, byte_code, args=[]):
        
        pc = 0 # program counter
        stack = []
        variables = [objects.Null()] * 255
        
        assert(len(args) == len(byte_code.arguments))
        
        #print "(running %s)" % byte_code.name
        
        # copy args into inner context
        for i in xrange(0,len(args)):
            # TODO: this doesn't make sense, indexes change I think?
            # Make sure these aren't getting overwritten
            index = byte_code.arguments[i]
            print "(arg %s going into %s)" % (args[i].dump(),index)
            byte_code.variables[index] = objects.Variable("arg",args[i])
            
        
        self.last_bc += byte_code.dump(True)
        
        while pc < len(byte_code.instructions):
            
            # the type of instruction and arg (a tuple)
            opcode, arg = byte_code.instructions[pc]
            
            #print "(%s %s %s)" % (pc, bytecode.reverse[opcode], arg)
            
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
                oldvar = byte_code.variables.get(arg,None)
                if isinstance(oldvar,objects.Variable):
                    byte_code.variables[arg] = objects.Variable(oldvar.name,value)
                else:
                    byte_code.variables[arg] = objects.Variable("arg",value)
                stack.append(value)
            
            elif opcode == bytecode.STORE_ARRAY:
                values = []
                for i in xrange(arg):
                    values.append(stack.pop())
                stack.append(objects.Array(values))
            
            elif opcode == bytecode.STORE_DICT:
                values = objects.r_dict(objects.dict_eq,objects.dict_hash)
                for i in xrange(arg):
                    values[stack.pop()] = stack.pop()
                stack.append(objects.Dict(values))
            
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
            
            elif opcode == bytecode.BINARY_NEQ:
                right = stack.pop()
                left = stack.pop()
                result = left.equals(right)
                result.boolvalue = not result.boolvalue
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
                assert(isinstance(byte_code.variables[arg],objects.Variable))
                val = byte_code.variables[arg].value
                if isinstance(val,objects.Function):
                    func = val.code
                    self.copy_context(byte_code,func)
                    args = []
                    if len(func.arguments) > len(stack):
                        raise Exception("Not enough arguments")
                    
                    for i in range(0,len(func.arguments)):
                        args.append(stack.pop())
                    stack.append(self.interpret(func,args))
                elif isinstance(val, objects.ExternalFunction):
                    # call
                    func = val.fn
                    arglen = val.args
                    args = []
                    for i in range(0,arglen):
                        args.append(stack.pop())
                    result = func(args)
                    stack.append(result)
                else:
                    raise Exception("Not a function")
        return stack[len(stack) - 1]
        

