from collections import OrderedDict
from evaler import evaluate
from parser import parse
from copy import copy

root_variables = OrderedDict()
learned_variables = OrderedDict()
variables = {}
facts = {}  # {varA:T. varB:F, } these are BOTH root variables and learned variables.
rules = []  # [ (if expression, then expression)... ]

# memoization = {
#     expression: Node
# }


#todo: make sure list is correct
def list():
    print('Root Variables:')
    for k,v in root_variables.items():
        print("\t{}={}".format(k,v))

    print('Learned Variables:')
    for k,v in learned_variables.items():
        print("\t{}={}".format(k,v))

    print('Facts:')
    for k in root_variables.keys():
        if facts[k]:
            print("\t{}".format(k))

    print('Rules:')
    for rule in rules:
        print("\t{}->{}".format(rule[0], rule[1]))

def teach(line):
    if '->' in line:
        teach_rule(line)
    elif '-R' in line:
        teach_variable(line, True)
    elif '-L' in line:
        teach_variable(line, False)
    else:
        assign(line)

def teach_variable(line, is_root):
    tokens = line.split(' ')
    variable = tokens[2]
    value = ' '.join(tokens[4:])

    if is_root:
        root_variables[variable] = value
        variables[variable] = value
    else:
        learned_variables[variable] = value
        variables[variable] = value
    facts[variable] = False

def assign(line):
    tokens = line.split(' ')
    decision = lambda v: True if v == 'true' else False
    if tokens[1] in root_variables:
        facts[tokens[1]] = decision(tokens[3].lower())

def teach_rule(line):
    if_part = line.split(' ')[1]
    then_part = line.split(' ')[3]

    assert then_part in learned_variables

    rules.append( (if_part, then_part) )

#Rule: (exp, variable)  represented if->then

def learn():
    # apply forward chaining to create new facts

    while True:
        changing = False
        for rule in rules:
            old = facts[rule[1]]
            facts[rule[1]] = evaluate( parse(rule[0]), facts)
            if facts[rule[1]] != old:
                changing = True
        if not changing:
            break

def query(line):
    global facts
    saved_facts = copy(facts)
    learn()
    exp = line.split(' ')[1]
    print( evaluate(parse(exp), facts) )
    facts = saved_facts


"""
PROF:
false
I KNOW IT IS NOT TRUE THAT Sam Likes Ice Cream
BECAUSE IT IS NOT TRUE THAT Sam Likes Ice Cream I CANNOT PROVE Sam Eats Ice Cream //when
concluding a rule cannot be proven
THUS I CANNOT PROVE (Sam Likes Ice Cream AND Sam Eats Ice Cream) //when concluding an
expression or sub-expression is false


GUY/GIRL:
I KNOW THAT "A"
BECAUSE "A" I KNOW THAT "B"
BECAUSE "A" AND ("B") I KNOW THAT "S"
I KNOW THAT "V"
I THUS KNOW THAT (("S") AND "V")
"""



def backtrack(node, facts):
    assert node is not None

    for rule in rules:
        if rule[1] == node.value:
            if node.value in root_variables.keys():
                # ROOT. THIS reveals root decision
                print('I KNOW IT IS {} THAT {}'.format(
                    'TRUE' if facts[node.value] else 'NOT TRUE',
                    node.value
                )
                )
                return facts[node.value]
            else:
                message = 'BECAUSE IT IS {} THAT {} I {} PROVE {}'
                if node.value == '!':
                    result = not backtrack(node.left, facts)
                    if result:
                        print(message.format(
                            'NOT TRUE',
                            variables[node.left.value],
                            'CAN',
                            variables[node.value]
                        ))
                        return True
                    else:
                        print(message.format(
                            'TRUE',
                            variables[node.left.value],
                            'CANNOT',
                            variables[node.value]
                        ))
                        return False


            if node.value in ['|', '&']:
                if node.value == '|':
                    back_track_left = backtrack(node.left, facts)
                    if back_track_left:
                        print(message.format(
                            'TRUE',
                            '{} OR {}'.format(variables[node.left.value], variables[node.right.value]),
                            'CAN',
                            variables[node.value]
                        ))
                        return True
                    else:
                        back_track_right = backtrack(node.right, facts)
                        if back_track_right:
                            print(message.format(
                                'TRUE',
                                '{} OR {}'.format(variables[node.left.value], variables[node.right.value]),
                                'CAN',
                                variables[node.value]
                            ))
                            return True
                        print(message.format(
                            'NOT TRUE',
                            '{} OR {}'.format(variables[node.left.value], variables[node.right.value]),
                            'CANNOT',
                            variables[node.value]
                        ))
                        return False
                elif node.value == '&':
                    back_track_left = backtrack(node.left, facts)
                    if back_track_left:
                        back_track_right = backtrack(node.right, facts)
                        if back_track_right:
                            print(message.format(
                                'TRUE',
                                '{} AND {}'.format(variables[node.left.value], variables[node.right.value]),
                                'CAN',
                                variables[node.value]
                            ))
                            return True
                        else:
                            print(message.format(
                                'NOT TRUE',
                                '{} AND {}'.format(variables[node.left.value], variables[node.right.value]),
                                'CANNOT',
                                variables[node.value]
                            ))
                            return False
                    else:
                        print(message.format(
                            'NOT TRUE',
                            '{} AND {}'.format(variables[node.left.value], variables[node.right.value]),
                            'CANNOT',
                            variables[node.value]
                        ))
                        return False

def why(line):
    exp = line.split(' ')[1]
    backtrack(parse(exp), facts)


if __name__=='__main__':

    while True:
        try:
            line = raw_input('')
        except EOFError:
            break
        command = line.split(' ')[0].lower()
        if 'teach' == command:
            teach(line)
        elif 'learn' == command:
            learn()
        elif 'list' == command:
            list()
        elif 'query' == command:
            query(line)
        elif 'why' == command:
            why(line)
        else:
            print('ERROR IN LINE: {myline}'.format(myline=line))
            break




#todo: make sure you check if user input is 'False', 'True'...
