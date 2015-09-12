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

    def test_parse_simple_or_not_and(self):
        a = Node(None, 'a', None)
        b = Node(None, 'b', None)
        c = Node(None, 'c', None)
        d = Node(None,'d',None)


        and_node = Node(c, '&', d)
        or_node = Node(a, '|',and_node)

        self.assertEqual(or_node, parse('a|(b&c)'))


    # todo:  a|b&c
    # todo:  (a|b)&c
    # todo:  a|(b&(c|d))
    # todo: !a & b
    # todo: !(a&b)
    # todo: a|b|c&d
    # todo: a|b|c|d
    # todo: !a|b|c|d

    # todo: !a|b|c

    # todo: !a|c
    #todo: tests with spaces in expression


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