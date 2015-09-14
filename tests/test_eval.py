from unittest import TestCase
from evaler import eval
import parser

__author__ = 'himanshu'


class TestEval(TestCase):



    def test_eval_basic(self):
        defined_variables = {
            'a': True
        }
        root = parser.parse('a')
        result = eval(root, defined_variables)
        self.assertEqual(result, True)

        defined_variables = {
            'a': False
        }
        root = parser.parse('a')
        result = eval(root, defined_variables)
        self.assertEqual(result, False)



    def test_eval_not(self):
        defined_variables = {
            'alpha': True
        }
        root = parser.parse('!alpha')
        result = eval(root, defined_variables)
        self.assertEqual(result, False)
    
        defined_variables = {
            'alpha': False
        }
        root = parser.parse('!alpha')
        result = eval(root, defined_variables)
        self.assertEqual(result, True)
    
    
    def test_eval_or(self):
        defined_variables = {
            'alpha': False,
            'b':False
        }
        root = parser.parse('alpha|b')
        result = eval(root, defined_variables)
        self.assertEqual(result, False)

        defined_variables = {
            'alpha': False,
            'b':True
        }
        root = parser.parse('alpha|b')
        result = eval(root, defined_variables)
        self.assertEqual(result, True)


        defined_variables = {
            'alpha': True,
            'b':False
        }
        root = parser.parse('alpha|b')
        result = eval(root, defined_variables)
        self.assertEqual(result, True)

        defined_variables = {
            'alpha': True,
            'b':True
        }
        root = parser.parse('alpha|b')
        result = eval(root, defined_variables)
        self.assertEqual(result, True)


    def test_eval_and(self):
        defined_variables = {
            'alpha': False,
            'b':False
        }
        root = parser.parse('alpha&b')
        result = eval(root, defined_variables)
        self.assertEqual(result, False)

        defined_variables = {
            'alpha': False,
            'b':True
        }
        root = parser.parse('alpha&b')
        result = eval(root, defined_variables)
        self.assertEqual(result, False)


        defined_variables = {
            'alpha': True,
            'b':False
        }
        root = parser.parse('alpha&b')
        result = eval(root, defined_variables)
        self.assertEqual(result, False)

        defined_variables = {
            'alpha': True,
            'b':True
        }
        root = parser.parse('alpha&b')
        result = eval(root, defined_variables)
        self.assertEqual(result, True)





