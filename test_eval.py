from unittest import TestCase
from evaler import evaluate
import parser

__author__ = 'himanshu'


class TestEval(TestCase):



    def test_eval_basic(self):
        defined_variables = {
            'a': True
        }
        root = parser.parse('a')
        result = evaluate(root, defined_variables)
        self.assertEqual(result, True)

        defined_variables = {
            'a': False
        }
        root = parser.parse('a')
        result = evaluate(root, defined_variables)
        self.assertEqual(result, False)



    def test_eval_not(self):
        defined_variables = {
            'alpha': True
        }
        root = parser.parse('!alpha')
        result = evaluate(root, defined_variables)
        self.assertEqual(result, False)
    
        defined_variables = {
            'alpha': False
        }
        root = parser.parse('!alpha')
        result = evaluate(root, defined_variables)
        self.assertEqual(result, True)
    
    
    def test_eval_or(self):
        defined_variables = {
            'alpha': False,
            'b':False
        }
        root = parser.parse('alpha|b')
        result = evaluate(root, defined_variables)
        self.assertEqual(result, False)

        defined_variables = {
            'alpha': False,
            'b':True
        }
        root = parser.parse('alpha|b')
        result = evaluate(root, defined_variables)
        self.assertEqual(result, True)


        defined_variables = {
            'alpha': True,
            'b':False
        }
        root = parser.parse('alpha|b')
        result = evaluate(root, defined_variables)
        self.assertEqual(result, True)

        defined_variables = {
            'alpha': True,
            'b':True
        }
        root = parser.parse('alpha|b')
        result = evaluate(root, defined_variables)
        self.assertEqual(result, True)


    def test_eval_and(self):
        defined_variables = {
            'alpha': False,
            'b':False
        }
        root = parser.parse('alpha&b')
        result = evaluate(root, defined_variables)
        self.assertEqual(result, False)

        defined_variables = {
            'alpha': False,
            'b':True
        }
        root = parser.parse('alpha&b')
        result = evaluate(root, defined_variables)
        self.assertEqual(result, False)


        defined_variables = {
            'alpha': True,
            'b':False
        }
        root = parser.parse('alpha&b')
        result = evaluate(root, defined_variables)
        self.assertEqual(result, False)

        defined_variables = {
            'alpha': True,
            'b':True
        }
        root = parser.parse('alpha&b')
        result = evaluate(root, defined_variables)
        self.assertEqual(result, True)


    def test_weird_breaking_thing(self):
        defined_variables = {
            'a': False,
            'b':False
        }
        root = parser.parse('(a|(!(a&a))|a&a|a)')
        result = evaluate(root, defined_variables)
        self.assertEqual(result, True)

    def test_weird_breaking_thing(self):
        defined_variables = {
            'a': False,
            'b':False
        }
        root = parser.parse('!a&a')
        result = evaluate(root, defined_variables)
        self.assertEqual(result, True)


