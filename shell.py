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
        print("\t{} = {}".format(k,v))

    print('Learned Variables:')
    for k,v in learned_variables.items():
        print("\t{} = {}".format(k,v))

    print('Facts:')
    for k in root_variables.keys():
        if facts[k]:
            print("\t{}".format(k))

    print('Rules:')
    for rule in rules:
        print("\t{} -> {}".format(rule[0], rule[1]))

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
        for var in facts.keys():
            if var in learned_variables:
                facts[var] = False
        # print(facts)
    else:
        raise TypeError

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

output_string = ""

def backtrack(node, facts):
    global output_string
    assert node is not None
    if node.value in root_variables.keys():
        # ROOT. THIS reveals root decision
        output_string += ('I KNOW IT IS {} THAT {}'.format(
            'TRUE' if facts[node.value] else 'NOT TRUE',
            variables[node.value]
            )
        ) + '\n'
        return facts[node.value]

    for rule in rules:
        # if rule[1] == node.value:

            if_part = parse(rule[0])
            if if_part.value in ['!','&','|']:
                message = 'BECAUSE IT IS {} THAT {} I {} PROVE {}'
                if if_part.value == '!':
                    result = not backtrack(if_part.left, facts)
                    if result:
                        output_string += (message.format(
                            'NOT TRUE',
                            variables[if_part.left.value],
                            'CAN',
                            variables[if_part.value]
                        )) + '\n'
                        return True
                    else:
                        output_string += (message.format(
                            'TRUE',
                            variables[if_part.left.value],
                            'CANNOT',
                            variables[if_part.value]
                        )) + '\n'
                        return False


                if if_part.value in ['|', '&']:
                    if if_part.value == '|':
                        back_track_left = backtrack(if_part.left, facts)
                        if back_track_left:
                            output_string += (message.format(
                                'TRUE',
                                '{} OR {}'.format(variables[if_part.left.value], variables[if_part.right.value]),
                                'CAN',
                                variables[if_part.value]
                            )) + '\n'
                            return True
                        else:
                            back_track_right = backtrack(if_part.right, facts)
                            if back_track_right:
                                output_string += (message.format(
                                    'TRUE',
                                    '{} OR {}'.format(variables[if_part.left.value], variables[if_part.right.value]),
                                    'CAN',
                                    variables[if_part.value]
                                )) + '\n'
                                return True
                            output_string += (message.format(
                                'NOT TRUE',
                                '{} OR {}'.format(variables[if_part.left.value], variables[if_part.right.value]),
                                'CANNOT',
                                variables[if_part.value]
                            )) + '\n'
                            return False
                    elif if_part.value == '&':
                        back_track_left = backtrack(if_part.left, facts)
                        if back_track_left:
                            back_track_right = backtrack(if_part.right, facts)
                            if back_track_right:
                                output_string += (message.format(
                                    'TRUE',
                                    '{} AND {}'.format(variables[if_part.left.value], variables[if_part.right.value]),
                                    'CAN',
                                    variables[if_part.value]
                                )) + '\n'
                                return True
                            else:
                                output_string += (message.format(
                                    'NOT TRUE',
                                    '{} AND {}'.format(variables[if_part.left.value], variables[if_part.right.value]),
                                    'CANNOT',
                                    variables[if_part.value]
                                )) + '\n'
                                return False
                        else:
                            output_string+=(message.format(
                                'NOT TRUE',
                                '{} AND {}'.format(variables[if_part.left.value], variables[if_part.right.value]),
                                'CANNOT',
                                variables[if_part.value]
                            ))+'\n'
                            return False
            else:

                # print(facts)
                # print(backtrack(if_part, facts))
                res = backtrack(if_part, facts)
                message = 'BECAUSE IT IS {} THAT {}, I {} PROVE {}'
                output_string+=(message.format(
                    'TRUE' if res else 'NOT TRUE',
                    variables[if_part.value],
                    'CAN' if res else 'CANNOT',
                    variables[rule[1]]

                ))+'\n'
                return res



def why(line):
    global output_string
    output_string = ""
    exp = line.split(' ')[1]
    result = backtrack(parse(exp), facts)
    message = 'THUS I {} PROVE ({})'
    print str(result).lower()
    print(output_string[:-1])
    print(message.format(
        'CAN' if result else 'CANNOT',
        node_to_string(parse(exp))
    ))

def node_to_string(root):

    if root.value == '!':
        return "NOT ({})".format(node_to_string(root.left))
    elif root.value == '|':
        return "{} OR {}".format(node_to_string(root.left), node_to_string(root.right))
    elif root.value == '&':
        return "{} AND {}".format(node_to_string(root.left), node_to_string(root.right))
    else:
        return variables[root.value]

def main():
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

if __name__=='__main__':
    main()






#todo: make sure you check if user input is 'False', 'True'...
