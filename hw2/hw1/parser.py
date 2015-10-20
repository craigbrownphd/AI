from Node import Node

"""
order of operations is ! & |
"""


def check_correct_string(str):
    return True
    #todo: implement me!

def is_op(char):
    assert isinstance(char, str)
    assert len(char) == 1
    return char in ['!', '&', '|']

# a|(b|(c|d))
# (a|b)|(c|d)
def char_index(expression=[]):

    # parantheticals are dropped to bottom
    # ! is dropped to right above paranthesis

    char_index.first_not = -1
    char_index.first_or = -1
    char_index.inside_paren = 0
    for i in range(0, len(expression)):


        if expression[i] == '(':
            char_index.inside_paren += 1
        elif expression[i] == ')':
            char_index.inside_paren -= 1


        if char_index.inside_paren == 0:
            if is_op(expression[i]):
                if expression[i] == '&':
                    return i
                elif expression[i]=='|':
                    if char_index.first_or == -1:
                        char_index.first_or = i
                elif expression[i] == '!':
                    if char_index.first_not == -1:
                        char_index.first_not = i

    # print('char_index.first_not = {}'.format(char_index.first_not))
    # print('char_index.first_or = {}'.format(char_index.first_or))
    if char_index.first_or != -1:
        return char_index.first_or
    else:
        return char_index.first_not




def parse(exp):
    if exp is None or exp == '':
        return None
    if exp[0] == '(' and exp[-1]==')':
        return parse(exp[1:-1])

    # strip spaces
    exp = exp.replace(" ","")

    special_index = char_index(exp)
    if special_index == -1:
        # assert len(exp) == 1
        return Node(None, exp, None)
    else:
        if exp[special_index] != '!':
            left = parse(exp[0:special_index])
            right = parse(exp[special_index+1:])
            return Node(left, exp[special_index], right)
        else:
            left = parse(exp[1:])
            return Node(left, '!', None)

