#from __future__ import unicode_literals
import unittest
import parser
import sys
from contextlib import contextmanager
from StringIO import StringIO

class Environment(object):
    
    def __init__(self):
        self.variables = {}


@contextmanager
def captured_output():
    new_out, new_err = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err


class ArithmeticTest(unittest.TestCase):
    
    def setUp(self):
        self.s = parser.ParserState()
        self.e = Environment()
    
    def test_primitives(self):
        result = parser.parse('5',self.s).eval(self.e)
        self.assertEqual(type(result),parser.Integer)
        self.assertEqual(result.to_string(), '5')
        
    def test_addition(self):        
        result = parser.parse('5 + 5',self.s).eval(self.e)
        self.assertEqual(type(result),parser.Integer)
        self.assertEqual(result.to_string(), '10')

    def test_negatives(self):        
        result = parser.parse('5 + -15',self.s).eval(self.e)
        self.assertEqual(result.to_string(), '-10')

    def test_subtraction(self):
        result = parser.parse('5 - 10',self.s).eval(self.e)
        self.assertEqual(result.to_string(), '-5')

    def test_multiplication(self):
        result = parser.parse('5 * 3',self.s).eval(self.e)
        self.assertEqual(result.to_string(), '15')
        
    def test_precedence(self):
        result = parser.parse('5 * 3 + 4',self.s).eval(self.e)
        self.assertEqual(result.to_string(), '19')
        result = parser.parse('5 + 3 * 4',self.s).eval(self.e)
        self.assertEqual(result.to_string(), '17')
        result = parser.parse('5 * (3 + 4)',self.s).eval(self.e)
        self.assertEqual(result.to_string(), '35')

    def test_floats(self):
        result = parser.parse('5 * 3.0',self.s).eval(self.e)
        self.assertEqual(result.to_string(), '15.0')

    def test_floats2(self):
        result = parser.parse('5.0 * -3.0',self.s).eval(self.e)
        self.assertEqual(result.to_string(), '-15.0')


class StringTest(unittest.TestCase):
    
    def setUp(self):
        self.s = parser.ParserState()
        self.e = Environment()
    
    def test_value(self):
        result = parser.parse('"a"',self.s).eval(self.e)
        self.assertEqual(result.to_string(), "a")

        result = parser.parse("'a'",self.s).eval(self.e)
        self.assertEqual(result.to_string(), "a")
        
        result = parser.parse('"""a b"""',self.s).eval(self.e)
        self.assertEqual(result.to_string(), "a b")
        
        result = parser.parse('"""a "b" c"""',self.s).eval(self.e)
        self.assertEqual(result.to_string(), 'a "b" c')

    def test_concat(self):
        result = parser.parse('"hi" + "yo"',self.s).eval(self.e)
        self.assertEqual(result.to_string(), "hiyo")
        

class BooleanTest(unittest.TestCase):
    
    def setUp(self):
        self.s = parser.ParserState()
        self.e = Environment()
    
    def test_values(self):
        result = parser.parse('true',self.s).eval(self.e)
        self.assertEqual(result.to_string(), 'true')
        result = parser.parse('false',self.s).eval(self.e)
        self.assertEqual(result.to_string(), 'false')
        
    def test_equality(self):
        result = parser.parse('true == true',self.s).eval(self.e)
        self.assertEqual(result.to_string(), 'true')
        result = parser.parse('false == false',self.s).eval(self.e)
        self.assertEqual(result.to_string(), 'true')
        result = parser.parse('true == false',self.s).eval(self.e)
        self.assertEqual(result.to_string(), 'false')

    def test_inequality(self):
        result = parser.parse('true != true',self.s).eval(self.e)
        self.assertEqual(result.to_string(), 'false')
        result = parser.parse('false != false',self.s).eval(self.e)
        self.assertEqual(result.to_string(), 'false')
        result = parser.parse('true != false',self.s).eval(self.e)
        self.assertEqual(result.to_string(), 'true')


class VariableTest(unittest.TestCase):
    
    def setUp(self):
        self.s = parser.ParserState()
        self.e = Environment()
    
    def test_assignment(self):
        result = parser.parse('a = 50',self.s).eval(self.e)
        self.assertEqual(result.to_string(), '50')
        result = parser.parse('a',self.s).eval(self.e)
        self.assertEqual(type(result), parser.Integer)
        self.assertEqual(result.to_string(), '50')
    
    def test_assignment_zero(self):
        result = parser.parse('k = 0',self.s).eval(self.e)
        self.assertEqual(result.to_string(), '0')
        result = parser.parse('k',self.s).eval(self.e)
        self.assertEqual(result.to_string(), '0')
   
    def test_assignment_string(self):
        result = parser.parse('l = "hey"',self.s).eval(self.e)
        self.assertEqual(result.to_string(), 'hey')
        result = parser.parse('l',self.s).eval(self.e)
        self.assertEqual(result.to_string(), "hey")
        
    def test_assignment_bool(self):
        result = parser.parse('o = true',self.s).eval(self.e)
        self.assertEqual(result.to_string(), 'true')
        result = parser.parse('o == true',self.s).eval(self.e)
        self.assertEqual(result.to_string(), "true")
        
    def test_multiples(self):
        result = parser.parse('m = 50',self.s).eval(self.e)
        self.assertEqual(result.to_string(), '50')
        result = parser.parse('n = m + 5',self.s).eval(self.e)
        self.assertEqual(result.to_string(), '55')
        result = parser.parse('n',self.s).eval(self.e)
        self.assertEqual(result.to_string(), '55')

    def test_multiline(self):
        code = """one = 5
                two = 10
                three = one + two
                print(three)"""
        with captured_output() as (out, err):
            result = parser.parse(code,self.s).eval(self.e)
            output = out.getvalue().strip()
        
        
        self.assertEqual(result.to_string(), '15')
        self.assertEqual(output, '15')
            
class PrintTest(unittest.TestCase):
    
    def setUp(self):
        self.s = parser.ParserState()
        self.e = Environment()
    
    def test_print_value(self):
        
        with captured_output() as (out, err):
            result = parser.parse('print(3)',self.s).eval(self.e)
            
            output = out.getvalue().strip()
            self.assertEqual(output, '3')
        
        with captured_output() as (out, err):
            result = parser.parse('print(3 * 5)',self.s).eval(self.e)
            
            output = out.getvalue().strip()
            self.assertEqual(output, '15')    
    
    def test_print_variable(self):
        with captured_output() as (out, err):
            result = parser.parse('a = 50.0',self.s).eval(self.e)
            result = parser.parse('print(a)',self.s).eval(self.e)
            
            output = out.getvalue().strip()
            self.assertEqual(output, '50.0')


class IfTest(unittest.TestCase):
    
    def setUp(self):
        self.s = parser.ParserState()
        self.e = Environment()
    
    def test_if(self):
        
        result = parser.parse('if true: true end',self.s).eval(self.e)
        self.assertEqual(result.to_string(), 'true')
    
        result = parser.parse('if false: true end',self.s).eval(self.e)
        self.assertEqual(type(result), parser.Noop)
    
    def test_if_else(self):
        
        result = parser.parse('if true: true else: false end',self.s).eval(self.e)
        self.assertEqual(result.to_string(), 'true')
    
        result = parser.parse('if 5 == 4: true else: false end',self.s).eval(self.e)
        self.assertEqual(result.to_string(), 'false')
    
    def test_multiline(self):
        code = """if true:
                    g = 5
                    print(15)
                end"""
        with captured_output() as (out, err):
            result = parser.parse(code,self.s).eval(self.e)
            output = out.getvalue().strip()
        
        self.assertEqual(result.to_string(), '15')
        self.assertEqual(output, '15')
    
    def test_multiline2(self):
        code = """a = 5
                if a == 4:
                    print(a)
                else:
                    b = 1
                    print("no")
                end"""
        with captured_output() as (out, err):
            result = parser.parse(code,self.s).eval(self.e)
            output = out.getvalue().strip()
        
        self.assertEqual(result.to_string(), 'no')
        self.assertEqual(output, 'no')

    def test_assignment(self):
        code = """a = 5
                b = if a == 4: a else: 1 end
                print(b)"""
        with captured_output() as (out, err):
            result = parser.parse(code,self.s).eval(self.e)
            output = out.getvalue().strip()
        
        self.assertEqual(result.to_string(), '1')
        self.assertEqual(output, '1')

if __name__ == '__main__':
    unittest.main()
