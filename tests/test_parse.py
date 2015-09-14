from unittest import TestCase
from parser import parse, char_index
from Node import Node


# ! & |
class TestParse(TestCase):

    def setUp(self):
        self.a = Node(None, 'a',None)
        self.b = Node(None, 'b',None)
        self.c = Node(None, 'c',None)
        self.d = Node(None, 'd',None)

    def test_parse_empty(self):
        self.assertEqual(None ,parse(''))
        self.assertEqual(None, parse(None))

    def test_parse_empty_parens(self):
        self.assertEqual(None, parse('()'))
        self.assertEqual(None, parse('(())'))
        self.assertEqual(None, parse('((()))'))
        # self.assertEqual(None, parse('(())()()()()()()()'))



    def test_parse_simple_letter(self):
        a = Node(None, 'a', None)
        self.assertEqual(a, parse('a'))

    def test_parse_simple_or(self):

        a = Node(None, 'a', None)
        b = Node(None, 'b', None)
        or_node = Node(a, '|', b)

        self.assertEqual(or_node, parse('a|b'))

    def test_parse_simple_and(self):

        a = Node(None, 'a', None)
        b = Node(None, 'b', None)
        and_node = Node(a, '&', b)

        self.assertEqual(and_node, parse('a&b'))


    def test_parse_simple_or_and(self):

        a = Node(None, 'a', None)
        b = Node(None, 'b', None)
        or_node = Node(a, '|', b)
        c = Node(None, 'c', None)
        and_node = Node(or_node, '&', c)

        self.assertEqual(and_node, parse('a|b&c'))

    def test_parse_complex_or_and_not(self):
        a = Node(None, 'a', None)
        b = Node(None, 'b', None)
        c = Node(None, 'c', None)
        d = Node(None,'d',None)



        not_node = Node(d, '!', None)

        or_node_left = Node(a, '|', b)
        or_node_right = Node(c, '|',not_node)
        and_node = Node(or_node_left, '&', or_node_right)

        self.assertEqual(and_node, parse('a|b&c|!d'))

    def test_parse_simple_or_not_and(self):
        a = Node(None, 'a', None)
        b = Node(None, 'b', None)
        c = Node(None, 'c', None)
        d = Node(None,'d',None)


        and_node = Node(c, '&', d)
        not_node = Node(and_node, '!', None)
        or_node_inner = Node(b, '|', not_node)
        or_node = Node(a, '|',or_node_inner)

        self.assertEqual(or_node, parse('a|b|!(c&d)'))

    def test_parse_paren(self):
        and_node = Node(self.b, '&', self.c)
        or_node = Node(self.a, '|',and_node)
        self.assertEqual(or_node, parse('a|(b&c)'))

    def test_parse_or_and(self):
        or_node = Node(self.a, '|', self.b)
        and_node = Node(or_node, '&', self.c)
        self.assertEqual(and_node, parse('a|b&c'))


    def test_parse_or_and_focus_due_to_paren(self):
        or_node = Node(self.a, '|', self.b)
        and_node = Node(or_node, '&', self.c)
        self.assertEqual(and_node, parse('a|b&c'))

    def test_parse_too_diff(self):
        inner_or_node = Node(self.c, '|', self.d)
        and_node = Node(self.b, '&', inner_or_node)
        or_node = Node(self.a, '|', and_node)
        self.assertEqual(or_node, parse('a|(b&(c|d))'))

    def test_parse_not_and(self):
        not_node = Node(self.a, '!', None)
        and_node = Node(not_node, '&', self.b)
        self.assertEqual(and_node, parse('!a&b'))

    def test_parse_not_and_with_spaces(self):
        not_node = Node(self.a, '!', None)
        and_node = Node(not_node, '&', self.b)
        self.assertEqual(and_node, parse('!a & b'))

    def test_parse_not_and_paren(self):
        and_node = Node(self.a, '&', self.b)
        not_node = Node(and_node, '!', None)
        self.assertEqual(not_node, parse('!(a&b)'))

    def test_parse_order_of_operations(self):
        right_or_node = Node(self.b, '|', self.c)
        left_or_node = Node(self.a, '|', right_or_node)
        and_node = Node(left_or_node, '&', self.d)
        self.assertEqual(and_node, parse('a|b|c&d'))

    def test_parse_multiple_or(self):
        right_or = Node(self.c, '|', self.d)
        middle_or = Node(self.b, '|', right_or)
        most_left_or = Node(self.a, '|', middle_or)
        self.assertEqual(most_left_or, parse('a|b|c|d'))

    def test_parse_multiple_and(self):
        right_and = Node(self.c, '&', self.d)
        middle_and = Node(self.b, '&', right_and)
        most_left_and = Node(self.a, '&', middle_and)
        self.assertEqual(most_left_and, parse('a&b&c&d'))

    def test_parse_multiple_or_with_twist(self):
        right_or = Node(self.c, '|', self.d)
        middle_or = Node(self.b, '|', right_or)
        not_node = Node(self.a, '!', None)
        most_left_or = Node(not_node, '|', middle_or)
        self.assertEqual(most_left_or, parse('!a|b|c|d'))

    def test_parse_simpler_twist(self):
        middle_or = Node(self.b, '|', self.c)
        not_node = Node(self.a, '!', None)
        most_left_or = Node(not_node, '|', middle_or)
        self.assertEqual(most_left_or, parse('!a|b|c'))

    def test_parse_simplest_twist(self):
        not_node = Node(self.a, '!', None)
        most_left_or = Node(not_node, '|', self.c)
        self.assertEqual(most_left_or, parse('!a|c'))

    def test_crazy_wild_spacing(self):
        or_node = Node(self.c, '|', self.d)
        not_node = Node(self.a, '!', None)
        and_node = Node(not_node, '&', or_node)
        outer_not = Node(and_node, '!',None)
        #!(!a&(c|d))
        self.assertEqual(outer_not, parse(' ! (    !  a& ( c | d ) )      '))

    #todo: test valid letter input

    def test_parse_long_variable_name(self):
        a = Node(None, 'alha', None)
        self.assertEqual(a, parse('alha'))


    def test_crazy_wild_spacing_with_long_names(self):
        a = Node(None, 'alpha', None)
        d = Node(None, 'dennis', None)
        c = Node(None, 'charlie', None)


        or_node = Node(c, '|', d)
        not_node = Node(a, '!', None)
        and_node = Node(not_node, '&', or_node)
        outer_not = Node(and_node, '!',None)
        #!(!a&(c|d))
        self.assertEqual(outer_not, parse(' ! (    !  alpha& ( charlie | dennis ) )      '))


    def test_char_index(self):
        mydict = {
            '!a':0,
            '!(a&b)':0,
            'a|b|c':1,
            'a|b&c':3,
            '!!!!a':0,
            '!a|!b':2,
            '(a|b)&c':5,
            'a|(b&c)':1,
        }
        for k,v in mydict.items():
            self.assertEquals(v, char_index(k), '{}->{}'.format(k,v))