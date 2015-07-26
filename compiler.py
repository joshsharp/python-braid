import bytecode, objects
import ast as ast_objects

class Context(object):
    """Shamelessly plundered from Cycy"""
    
    def __init__(self):
        self.instructions = []
        self.constants = []
        self.variables = {}
        self.functions = {}
        
        self.NULL = self.register_constant(objects.Null())
        self.TRUE = self.register_constant(objects.Boolean(True))
        self.FALSE = self.register_constant(objects.Boolean(False))
        
    def emit(self, byte_code, arg=bytecode.NO_ARG):
        self.instructions.append(byte_code)
        self.instructions.append(arg)

    def register_variable(self, name):
        self.variables[name] = len(self.variables)
        return len(self.variables) - 1

    def register_function(self, name, index, arg_count):
        self.functions[name] = (index, arg_count)

    def register_constant(self, constant):
        self.constants.append(constant)
        return len(self.constants) - 1

    def build(self, arguments=[], name="<input>"):
        return bytecode.Bytecode(
            instructions=self.instructions,
            name=name,
            arguments=arguments,
            constants=self.constants,
            variables=self.variables,
        )


def compile_program(context, ast):
    for statement in ast.get_statements():
        compile_any(context,statement)


def compile_functiondeclaration(context, ast):
    # new context, but need access to outer context
    # TODO: this seems wrong, maybe we need the outer context
    # to be a 'parent' instead of merging them
    # then work up through them as needed
    ctx = Context()
    ctx.constants = context.constants
    ctx.variables = context.variables
    ctx.functions = context.functions
    
    arg_count = 0
    
    if type(ast.args) is not ast_objects.Null:
        
        arg_count = len(ast.args.get_statements())
        
        for arg in ast.args.get_statements():
            # TODO: need a way to say these names are to be
            # filled by literal arguments when this is called.
            pass
        
    compile_block(ctx,ast.block)
    
    fn = context.register_constant(ctx.build(name=ast.name.name))
    context.register_function(ast.name.name, fn, arg_count)
    context.emit(bytecode.LOAD_CONST,0)


def compile_function(context, ast):
    # this is a call really
    
    if type(ast.args) is ast_objects.InnerArray:
    
        for arg in ast.args.statements:
            compile_any(context, arg)
    
    index = context.functions.get(ast.name.name, None)
    if index:
        context.emit(bytecode.CALL, index)
    else:
        raise Exception("function does not exist")


def compile_block(context, ast):
    for statement in ast.get_statements():
        compile_any(context,statement)


def compile_innerarray(context, ast):
    # this is used for function args I think
    for statement in ast.get_statements():
        compile_any(context,statement)


def compile_array(context, ast):
    for statement in ast.get_statements():
        compile_any(context,statement)


def compile_null(context, ast):
    context.emit(bytecode.LOAD_CONST,0)


def compile_boolean(context, ast):
    value = objects.Boolean(ast.value)
    index = context.register_constant(value)
    
    context.emit(bytecode.LOAD_CONST,index)


def compile_integer(context, ast):
    value = objects.Integer(ast.value)
    index = context.register_constant(value)
    
    context.emit(bytecode.LOAD_CONST,index)


def compile_float(context, ast):
    value = objects.Float(ast.value)
    index = context.register_constant(value)
    
    context.emit(bytecode.LOAD_CONST,index)


def compile_string(context, ast):
    value = objects.String(ast.value)
    index = context.register_constant(value)
    
    context.emit(bytecode.LOAD_CONST,index)


def compile_variable(context, ast):
    index = context.variables.get(ast.name,bytecode.NO_ARG)
    if index > bytecode.NO_ARG:
        context.emit(bytecode.LOAD_VARIABLE,index)
    else:
        raise Exception("Attempt to use undefined variable %s" % ast.name)

def compile_print(context, ast):
    compile_any(context,ast.value)
    context.emit(bytecode.PRINT,bytecode.NO_ARG)


def compile_if(context, ast):
    # compile the condition
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
    context.instructions[false_jump] = false_block
    compile_any(context,ast.else_body)
    # get the point we're at now
    after_false = len(context.instructions)
    # then change the true jump to point here
    context.instructions[false_block-1] = after_false


def compile_equal(context, ast):
    compile_any(context, ast.right)
    compile_any(context, ast.left)
    context.emit(bytecode.BINARY_EQ,bytecode.NO_ARG)


def compile_notequal(context, ast):
    compile_any(context, ast.right)
    compile_any(context, ast.left)
    context.emit(bytecode.BINARY_NEQ,bytecode.NO_ARG)


def compile_greaterthan(context, ast):
    compile_any(context, ast.right)
    compile_any(context, ast.left)
    context.emit(bytecode.BINARY_GT,bytecode.NO_ARG)


def compile_greaterthanequal(context, ast):
    compile_any(context, ast.right)
    compile_any(context, ast.left)
    context.emit(bytecode.BINARY_GTE,bytecode.NO_ARG)


def compile_lessthan(context, ast):
    compile_any(context, ast.right)
    compile_any(context, ast.left)
    context.emit(bytecode.BINARY_LT,bytecode.NO_ARG)


def compile_lessthanequal(context, ast):
    compile_any(context, ast.right)
    compile_any(context, ast.left)
    context.emit(bytecode.BINARY_LTE,bytecode.NO_ARG)


def compile_and(context, ast):
    compile_any(context, ast.right)
    compile_any(context, ast.left)
    context.emit(bytecode.BINARY_AND,bytecode.NO_ARG)


def compile_or(context, ast):
    compile_any(context, ast.right)
    compile_any(context, ast.left)
    context.emit(bytecode.BINARY_OR,bytecode.NO_ARG)


def compile_not(context, ast):
    compile_any(context, ast.value)
    context.emit(bytecode.NOT,bytecode.NO_ARG)


def compile_add(context, ast):
    compile_any(context, ast.right)
    compile_any(context, ast.left)
    context.emit(bytecode.BINARY_ADD,bytecode.NO_ARG)


def compile_sub(context, ast):
    compile_any(context, ast.right)
    compile_any(context, ast.left)
    context.emit(bytecode.BINARY_SUB,bytecode.NO_ARG)


def compile_mul(context, ast):
    compile_any(context, ast.right)
    compile_any(context, ast.left)
    context.emit(bytecode.BINARY_MUL,bytecode.NO_ARG)


def compile_div(context, ast):
    compile_any(context, ast.right)
    compile_any(context, ast.left)
    context.emit(bytecode.BINARY_DIV,bytecode.NO_ARG)


def compile_assignment(context, ast):
    index = context.register_variable(ast.left.name)
    compile_any(context, ast.right)
    context.emit(bytecode.STORE_VARIABLE, index)


def compile_index(context, ast):
    compile_any(context, ast.right)
    compile_any(context, ast.left)
    context.emit(bytecode.BINARY_INDEX,bytecode.NO_ARG)


def compile_any(context, ast):
    typename = ast.__class__.__name__
    funcname = "compile_%s" % typename.lower()
    
    func = globals().get(funcname,None)
    if func:
        func(context, ast)
    else:
        raise Exception("Cannot compile %s - cannot find %s" % (typename, funcname))


def compile(ast, context=None):
    """
    Begin here.
    """
    if context is None:
        context = Context()
    
    compile_any(context, ast)
    context.emit(bytecode.RETURN,1)
    
    return context.build()
