#from __future__ import unicode_literals
import unittest
import parser
import sys
from contextlib import contextmanager
from StringIO import StringIO

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
    
    def test_primitives(self):
        result = parser.parse('5').eval()
        self.assertEqual(type(result),parser.Integer)
        self.assertEqual(result.to_string(), '5')
        
    def test_addition(self):        
        result = parser.parse('5 + 5').eval()
        self.assertEqual(type(result),parser.Integer)
        self.assertEqual(result.to_string(), '10')

    def test_negatives(self):        
        result = parser.parse('5 + -15').eval()
        self.assertEqual(result.to_string(), '-10')

    def test_subtraction(self):
        result = parser.parse('5 - 10').eval()
        self.assertEqual(result.to_string(), '-5')

    def test_multiplication(self):
        result = parser.parse('5 * 3').eval()
        self.assertEqual(result.to_string(), '15')
        
    def test_precedence(self):
        result = parser.parse('5 * 3 + 4').eval()
        self.assertEqual(result.to_string(), '19')
        result = parser.parse('5 + 3 * 4').eval()
        self.assertEqual(result.to_string(), '17')
        result = parser.parse('5 * (3 + 4)').eval()
        self.assertEqual(result.to_string(), '35')

    def test_floats(self):
        result = parser.parse('5 * 3.0').eval()
        self.assertEqual(result.to_string(), '15.0')

    def test_floats2(self):
        result = parser.parse('5.0 * -3.0').eval()
        self.assertEqual(result.to_string(), '-15.0')


class StringTest(unittest.TestCase):
    
    def test_value(self):
        result = parser.parse('"a"').eval()
        self.assertEqual(result.to_string(), "a")

        result = parser.parse("'a'").eval()
        self.assertEqual(result.to_string(), "a")
        
        result = parser.parse('"""a b"""').eval()
        self.assertEqual(result.to_string(), "a b")
        
        result = parser.parse('"""a "b" c"""').eval()
        self.assertEqual(result.to_string(), 'a "b" c')

    def test_concat(self):
        result = parser.parse('"hi" + "yo"').eval()
        self.assertEqual(result.to_string(), "hiyo")
        

class BooleanTest(unittest.TestCase):
    
    def test_values(self):
        result = parser.parse('true').eval()
        self.assertEqual(result.to_string(), 'true')
        result = parser.parse('false').eval()
        self.assertEqual(result.to_string(), 'false')
        
    def test_equality(self):
        result = parser.parse('true == true').eval()
        self.assertEqual(result.to_string(), 'true')
        result = parser.parse('false == false').eval()
        self.assertEqual(result.to_string(), 'true')
        result = parser.parse('true == false').eval()
        self.assertEqual(result.to_string(), 'false')

    def test_inequality(self):
        result = parser.parse('true != true').eval()
        self.assertEqual(result.to_string(), 'false')
        result = parser.parse('false != false').eval()
        self.assertEqual(result.to_string(), 'false')
        result = parser.parse('true != false').eval()
        self.assertEqual(result.to_string(), 'true')


class VariableTest(unittest.TestCase):
    
    def test_assignment(self):
        result = parser.parse('j = 50').eval()
        self.assertEqual(result.to_string(), '50')
        result = parser.parse('j').eval()
        self.assertEqual(type(result), parser.Integer)
        self.assertEqual(result.to_string(), '50')
    
    def test_assignment_zero(self):
        result = parser.parse('k = 0').eval()
        self.assertEqual(result.to_string(), '0')
        result = parser.parse('k').eval()
        self.assertEqual(result.to_string(), '0')
   
    def test_assignment_string(self):
        result = parser.parse('l = "hey"').eval()
        self.assertEqual(result.to_string(), 'hey')
        result = parser.parse('l').eval()
        self.assertEqual(result.to_string(), "hey")
        
    def test_assignment_bool(self):
        result = parser.parse('o = true').eval()
        self.assertEqual(result.to_string(), 'true')
        result = parser.parse('o == true').eval()
        self.assertEqual(result.to_string(), "true")
        
    def test_multiples(self):
        result = parser.parse('m = 50').eval()
        self.assertEqual(result.to_string(), '50')
        result = parser.parse('n = m + 5').eval()
        self.assertEqual(result.to_string(), '55')
        result = parser.parse('n').eval()
        self.assertEqual(result.to_string(), '55')


class PrintTest(unittest.TestCase):
    
    def test_print_value(self):
        
        with captured_output() as (out, err):
            result = parser.parse('print(3)').eval()
            
            output = out.getvalue().strip()
            self.assertEqual(output, '3')
        
        with captured_output() as (out, err):
            result = parser.parse('print(3 * 5)').eval()
            
            output = out.getvalue().strip()
            self.assertEqual(output, '15')    
    
    def test_print_variable(self):
        with captured_output() as (out, err):
            result = parser.parse('a = 50.0').eval()
            result = parser.parse('print(a)').eval()
            
            output = out.getvalue().strip()
            self.assertEqual(output, '50.0')

if __name__ == '__main__':
    unittest.main()
