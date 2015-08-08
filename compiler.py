import bytecode, objects, errors
import ast as ast_objects

class Context(object):
    """Shamelessly plundered from Cycy"""
    
    def __init__(self):
        self.instructions = []
        self.constants = []
        self.variables = {}
        
        #self.NULL = self.register_constant(objects.Null())
        #self.TRUE = self.register_constant(objects.Boolean(True))
        #self.FALSE = self.register_constant(objects.Boolean(False))
        
    def emit(self, byte_code, arg=bytecode.NO_ARG):
        assert(isinstance(byte_code,int))
        assert(isinstance(arg,int))
        self.instructions.append((byte_code,arg))

    def register_variable(self, name):
        index = len(self.variables)
        self.variables[index] = objects.Variable(name,objects.Null())
        return index

    def register_constant(self, constant):
        index = len(self.constants)
        self.constants.append(constant)
        return index

    def register_function(self, function):
        index = len(self.functions)
        self.functions[index] = function
        return index
    
    def build(self, arguments=[], name="<input>"):
        
        if isinstance(arguments, ast_objects.Null):
            arguments = []
        elif isinstance(arguments, ast_objects.Array):
            arguments = [s.getname() for s in arguments.getstatements()]
        
        return bytecode.Bytecode(
            instructions=self.instructions,
            name=name,
            arguments=arguments,
            constants=self.constants,
            variables=self.variables,
        )


def compile_program(context, ast):
    assert(isinstance(ast,ast_objects.Program))
    for statement in ast.get_statements():
        compile_any(context,statement)


def compile_functiondeclaration(context, ast):
    assert(isinstance(ast,ast_objects.FunctionDeclaration))
    # new context, but need access to outer context
    ctx = Context()
    
    fn_index = context.register_variable(ast.name)
    
    for v in context.constants:
        ctx.constants.append(v)
    for k, v in context.variables.iteritems():
        ctx.variables[k] = v
    
    indexes = []
    
    if type(ast.args) is not ast_objects.Null:
        
        for arg in reversed(ast.args.get_statements()):
            assert(isinstance(arg,ast_objects.Variable))
            name = str(arg.getname())
            index = ctx.register_variable(name)
            indexes.append(index)
            #context.emit(bytecode.STORE_VARIABLE, index)
        
    compile_block(ctx,ast.block)
    
    fn = ctx.build(indexes, name=ast.name)
    context.variables[fn_index] = objects.Variable(ast.name,objects.Function(ast.name,fn))
    ctx.variables[fn_index] = objects.Variable(ast.name,objects.Function(ast.name,fn))
    context.emit(bytecode.LOAD_VARIABLE,fn_index)


def compile_function(context, ast):
    assert(isinstance(ast,ast_objects.Function))
    # this is a call really
    
    if type(ast.args) is ast_objects.InnerArray:
    
        for arg in ast.args.get_statements():
            compile_any(context, arg)
    
    index = -1
    for k, v in context.variables.iteritems():
        assert(isinstance(v, objects.Variable))
        #assert(isinstance(v.value, objects.Function))
        if v.name == ast.name:
            index = k
    if index > -1:
        context.emit(bytecode.CALL, index)
    else:
        raise Exception("function %s does not exist" % ast.name)


def compile_block(context, ast):
    assert(isinstance(ast,ast_objects.Block))
    for statement in ast.get_statements():
        compile_any(context,statement)


def compile_innerarray(context, ast):
    assert(isinstance(ast,ast_objects.InnerArray))
    # this is used for function args I think
    for statement in ast.get_statements():
        compile_any(context,statement)


def compile_array(context, ast):
    assert(isinstance(ast,ast_objects.Array))
    length = len(ast.get_statements())
    for statement in reversed(ast.get_statements()):
        compile_any(context,statement)
    context.emit(bytecode.STORE_ARRAY,length)


def compile_innerdict(context, ast):
    assert(isinstance(ast,ast_objects.InnerDict))
    for key, val in ast.get_statements().iteritems():
        compile_any(context,key)
        compile_any(context,val)


def compile_dict(context, ast):
    assert(isinstance(ast,ast_objects.Dict))
    length = len(ast.get_statements().keys())
    for key, val in ast.get_statements().iteritems():
        print "add key %s" % key.rep()
        compile_any(context,key)
        print "add val %s" % val.rep()
        compile_any(context,val)
    context.emit(bytecode.STORE_DICT,length)


def compile_null(context, ast):
    assert(isinstance(ast,ast_objects.Null))
    context.emit(bytecode.LOAD_CONST,0)


def compile_boolean(context, ast):
    assert(isinstance(ast,ast_objects.Boolean))
    value = objects.Boolean(ast.value)
    index = context.register_constant(value)
    
    context.emit(bytecode.LOAD_CONST,index)


def compile_integer(context, ast):
    assert(isinstance(ast,ast_objects.Integer))
    value = objects.Integer(ast.value)
    index = context.register_constant(value)
    
    context.emit(bytecode.LOAD_CONST,index)


def compile_float(context, ast):
    assert(isinstance(ast,ast_objects.Float))
    value = objects.Float(ast.value)
    index = context.register_constant(value)
    
    context.emit(bytecode.LOAD_CONST,index)


def compile_string(context, ast):
    assert(isinstance(ast,ast_objects.String))
    value = objects.String(ast.value)
    index = context.register_constant(value)    
    context.emit(bytecode.LOAD_CONST,index)


def compile_variable(context, ast):
    assert(isinstance(ast,ast_objects.Variable))
    index = None
    for k, v in context.variables.iteritems():
        assert(isinstance(v,objects.Variable))
        if v.name == ast.getname():
            index = k
            break
    if index is not None:
        context.emit(bytecode.LOAD_VARIABLE,index)
    else:
        raise Exception("Variable %s not yet defined" % ast.getname())
    

def compile_print(context, ast):
    assert(isinstance(ast,ast_objects.Print))
    compile_any(context,ast.value)
    context.emit(bytecode.PRINT,bytecode.NO_ARG)


def compile_if(context, ast):
    # compile the condition
    assert(isinstance(ast, ast_objects.If))
    compile_any(context, ast.condition)
    # add true
    t = context.register_constant(objects.Boolean(True))
    context.emit(bytecode.LOAD_CONST,t)
    # compare the condition to true
    context.emit(bytecode.BINARY_EQ,bytecode.NO_ARG)
    
    # condition:
    # jump if zero (false): false block
    # true block
    # jump to end
    # false block
    
    # TODO: let jump target labels, not values! store the name of the jump
    # in a constant and then reference that constant name, which can contain the
    # jump position and be updated if need be
    
    context.emit(bytecode.JUMP_IF_ZERO,0)
    # make a note of the instruction we'll have to change
    false_jump = len(context.instructions) - 1
    # then add the true block
    compile_any(context,ast.body)
    # then a jump from the true block to after the false block
    context.emit(bytecode.JUMP,0)
    # the start of the false block is the current length
    false_block = len(context.instructions)
    # so set the false block jump to that point
    context.instructions[false_jump] = (context.instructions[false_jump][0],false_block)
    compile_any(context,ast.else_body)
    # get the point we're at now
    after_false = len(context.instructions)
    # then change the true jump to point here
    context.instructions[false_block-1] = (context.instructions[false_block-1][0], after_false)


def compile_while(context, ast):
    assert(isinstance(ast, ast_objects.While))
    condition_pos = len(context.instructions)
    compile_any(context, ast.condition)
    # add true
    t = context.register_constant(objects.Boolean(True))
    context.emit(bytecode.LOAD_CONST,t)
    # compare the condition to true
    context.emit(bytecode.BINARY_EQ,bytecode.NO_ARG)
    
    # condition:
    # jump if zero (false): after the block
    # block
    # jump to condition
    
    # this will point to after the end
    context.emit(bytecode.JUMP_IF_ZERO,0)
    # make a note of the instruction we'll have to change
    false_jump = len(context.instructions) - 1
    compile_any(context,ast.body)
    context.emit(bytecode.JUMP,condition_pos)
    after_block = len(context.instructions)
    context.instructions[false_jump] = (context.instructions[false_jump][0],after_block)


def compile_equal(context, ast):
    assert(isinstance(ast,ast_objects.Equal))
    compile_any(context, ast.left)
    compile_any(context, ast.right)
    context.emit(bytecode.BINARY_EQ,bytecode.NO_ARG)


def compile_notequal(context, ast):
    assert(isinstance(ast,ast_objects.NotEqual))
    compile_any(context, ast.left)
    compile_any(context, ast.right)
    context.emit(bytecode.BINARY_NEQ,bytecode.NO_ARG)


def compile_greaterthan(context, ast):
    assert(isinstance(ast,ast_objects.GreaterThan))
    compile_any(context, ast.left)
    compile_any(context, ast.right)
    context.emit(bytecode.BINARY_GT,bytecode.NO_ARG)


def compile_greaterthanequal(context, ast):
    assert(isinstance(ast,ast_objects.GreaterThanEqual))
    compile_any(context, ast.left)
    compile_any(context, ast.right)
    context.emit(bytecode.BINARY_GTE,bytecode.NO_ARG)


def compile_lessthan(context, ast):
    assert(isinstance(ast,ast_objects.LessThan))
    compile_any(context, ast.left)
    compile_any(context, ast.right)
    context.emit(bytecode.BINARY_LT,bytecode.NO_ARG)


def compile_lessthanequal(context, ast):
    assert(isinstance(ast,ast_objects.LessThanEqual))
    compile_any(context, ast.left)
    compile_any(context, ast.right)
    context.emit(bytecode.BINARY_LTE,bytecode.NO_ARG)


def compile_and(context, ast):
    assert(isinstance(ast,ast_objects.And))
    compile_any(context, ast.left)
    compile_any(context, ast.right)
    context.emit(bytecode.BINARY_AND,bytecode.NO_ARG)


def compile_or(context, ast):
    assert(isinstance(ast,ast_objects.Or))
    compile_any(context, ast.left)
    compile_any(context, ast.right)
    context.emit(bytecode.BINARY_OR,bytecode.NO_ARG)


def compile_not(context, ast):
    assert(isinstance(ast,ast_objects.Not))
    compile_any(context, ast.value)
    context.emit(bytecode.NOT,bytecode.NO_ARG)


def compile_add(context, ast):
    assert(isinstance(ast,ast_objects.Add))
    compile_any(context, ast.left)
    compile_any(context, ast.right)
    context.emit(bytecode.BINARY_ADD,bytecode.NO_ARG)


def compile_sub(context, ast):
    assert(isinstance(ast,ast_objects.Sub))    
    compile_any(context, ast.left)
    compile_any(context, ast.right)
    context.emit(bytecode.BINARY_SUB,bytecode.NO_ARG)


def compile_mul(context, ast):
    assert(isinstance(ast,ast_objects.Mul))
    compile_any(context, ast.left)
    compile_any(context, ast.right)
    context.emit(bytecode.BINARY_MUL,bytecode.NO_ARG)


def compile_div(context, ast):
    assert(isinstance(ast,ast_objects.Div))
    compile_any(context, ast.left)
    compile_any(context, ast.right)
    context.emit(bytecode.BINARY_DIV,bytecode.NO_ARG)


def compile_assignment(context, ast):
    assert(isinstance(ast,ast_objects.Assignment))
    assert(isinstance(ast.left,ast_objects.Variable))
    
    name = str(ast.left.getname())
    index = None
    for k, v in context.variables.iteritems():
        if v.name == name:
            index = k
            raise errors.ImmutableError(name)

    if index is None:        
        index = context.register_variable(name)
    compile_any(context, ast.right)
    context.emit(bytecode.STORE_VARIABLE, index)


def compile_argument(context, name):
    
    index = context.register_variable(str(name))
    context.emit(bytecode.STORE_VARIABLE, index)


def compile_index(context, ast):
    assert(isinstance(ast,ast_objects.Index))
    compile_any(context, ast.right)
    compile_any(context, ast.left)
    context.emit(bytecode.INDEX,bytecode.NO_ARG)


def compile_any(context, ast):
    typename = ast.__class__.__name__.lower()
    #funcname = "compile_%s" % typename.lower()
    
    funcs = {
        "index":compile_index,
        "div":compile_div,
        "sub":compile_sub,
        "mul":compile_mul,
        "assignment":compile_assignment,
        "argument":compile_argument,
        "add":compile_add,
        "function":compile_function,
        "functiondeclaration":compile_functiondeclaration,
        "block":compile_block,
        "or":compile_or,
        "and":compile_and,
        "not":compile_not,
        "print":compile_print,
        "string":compile_string,
        "integer":compile_integer,
        "float":compile_float,
        "boolean":compile_boolean,
        "array":compile_array,
        "innerarray":compile_innerarray,
        "dict":compile_dict,
        "innerdict":compile_dict,
        "program":compile_program,
        "null":compile_null,
        "variable":compile_variable,
        "if":compile_if,
        "while":compile_while,
        "greaterthan":compile_greaterthan,
        "greaterthanequal":compile_greaterthanequal,
        "lessthan":compile_lessthan,
        "lessthanequal":compile_lessthanequal,
        "equal":compile_equal,
    }
    
    func = funcs.get(typename,None)
    if func:
        func(context, ast)
    else:
        raise Exception("Cannot compile %s - cannot find it" % (typename))


def compile(ast, context=None):
    """
    Begin here.
    """
    if context is None:
        context = Context()
    
    compile_any(context, ast)
    context.emit(bytecode.RETURN,1)
    
    return context.build()
