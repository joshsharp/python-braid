import bytecode, objects, errors
import ast as ast_objects

class Context(object):
    """Shamelessly plundered from Cycy"""
    
    def __init__(self):
        self.instructions = []
        self.constants = {}
        self.variables = {}
        
        self.NULL = self.register_constant(objects.Null())
        self.TRUE = self.register_constant(objects.Boolean(True))
        self.FALSE = self.register_constant(objects.Boolean(False))
        
    def emit(self, byte_code, arg=bytecode.NO_ARG):
        assert(isinstance(byte_code,int))
        self.instructions.append(byte_code)
        args = str(arg)
        self.instructions.append(args)

    def register_variable(self, name):
        self.variables[str(name)] = objects.Null()
        return str(name)

    def register_constant(self, constant, name=None):
        if not name:
            name = len(self.constants)
        self.constants[str(name)] = constant        
        return str(name)

    def build(self, arguments=None, name="<input>"):
        
        if arguments is None:
            arguments = []
        if type(arguments) is ast_objects.Null:
            arguments = []
        elif type(arguments) is ast_objects.Array:
            arguments = arguments.statements
        
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
    # TODO: this seems wrong, maybe we need the outer context
    # to be a 'parent' instead of merging them
    # then work up through them as needed
    ctx = Context()
    for k, v in context.constants.iteritems():
        ctx.constants[k] = v
    for k, v in context.variables.iteritems():
        ctx.variables[k] = v

    #arg_count = 0
    #
    if type(ast.args) is not ast_objects.Null:
        
        arg_count = len(ast.args.get_statements())
        
        for arg in ast.args.get_statements():
            assert(isinstance(arg,ast_objects.Variable))
            name = str(arg.getname())
            # TODO: need a way to say these names are to be
            # filled by literal arguments when this is called.
            ctx.variables[name] = objects.Null()
        
    compile_block(ctx,ast.block)
    
    fn = ctx.build(ast.args, name=ast.name)
    context.register_constant(fn, ast.name)
    context.emit(bytecode.LOAD_CONST,0)


def compile_function(context, ast):
    assert(isinstance(ast,ast_objects.Function))
    # this is a call really
    
    if type(ast.args) is ast_objects.InnerArray:
    
        for arg in ast.args.get_statements():
            compile_any(context, arg)
    
    #print "calling %s" % ast.name.name
    fn = context.constants.get(ast.name.name, None)
    if fn:
        context.emit(bytecode.CALL, ast.name.name)
    else:
        raise Exception("function does not exist")


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
    for statement in ast.get_statements():
        compile_any(context,statement)


def compile_null(context, ast):
    assert(isinstance(ast,ast_objects.Null))
    context.emit(bytecode.LOAD_CONST,"0")


def compile_boolean(context, ast):
    assert(isinstance(ast,ast_objects.Boolean))
    value = objects.Boolean(ast.value)
    index = context.register_constant(value)
    
    context.emit(bytecode.LOAD_CONST,str(index))


def compile_integer(context, ast):
    assert(isinstance(ast,ast_objects.Integer))
    value = objects.Integer(ast.value)
    index = context.register_constant(value)
    
    context.emit(bytecode.LOAD_CONST,str(index))


def compile_float(context, ast):
    assert(isinstance(ast,ast_objects.Float))
    value = objects.Float(ast.value)
    index = context.register_constant(value)
    
    context.emit(bytecode.LOAD_CONST,str(index))


def compile_string(context, ast):
    assert(isinstance(ast,ast_objects.String))
    value = objects.String(ast.value)
    index = context.register_constant(value)    
    context.emit(bytecode.LOAD_CONST,str(index))


def compile_variable(context, ast):
    assert(isinstance(ast,ast_objects.Variable))
    context.emit(bytecode.LOAD_VARIABLE,ast.name)
    

def compile_print(context, ast):
    assert(isinstance(ast,ast_objects.Print))
    compile_any(context,ast.value)
    context.emit(bytecode.PRINT,bytecode.NO_ARG)


def compile_if(context, ast):
    # compile the condition
    assert(isinstance(ast, ast_objects.If))
    compile_any(context, ast.condition)
    # add true
    context.emit(bytecode.LOAD_CONST,context.TRUE)
    # compare the condition to true
    context.emit(bytecode.BINARY_EQ,bytecode.NO_ARG)
    
    # condition:
    # jump if zero: false block
    # true block
    # jump to end
    # false block
    
    # TODO: let jump target labels, not values! store the name of the jump
    # in a constant and then reference that constant name, which can contain the
    # jump position and be updated if need be
    
    context.emit(bytecode.JUMP_IF_ZERO,"0")
    # make a note of the instruction we'll have to change
    false_jump = len(context.instructions) - 1
    # then add the true block
    compile_any(context,ast.body)
    # then a jump from the true block to after the false block
    context.emit(bytecode.JUMP,"0")
    # the start of the false block is the current length
    false_block = len(context.instructions)
    # so set the false block jump to that point
    context.instructions[false_jump] = str(false_block)
    compile_any(context,ast.else_body)
    # get the point we're at now
    after_false = len(context.instructions)
    # then change the true jump to point here
    context.instructions[false_block-1] = str(after_false)


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
    
    index = context.register_variable(name)
    compile_any(context, ast.right)
    context.emit(bytecode.STORE_VARIABLE, str(index))


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
        "boolean":compile_boolean,
        "array":compile_array,
        "innerarray":compile_innerarray,
        "program":compile_program,
        "null":compile_null,
        "variable":compile_variable,
        "if":compile_if,
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
    context.emit(bytecode.RETURN,"1")
    
    return context.build()
