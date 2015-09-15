from collections import OrderedDict
from evaler import evaluate
from parser import parse
from copy import copy

root_variables = OrderedDict()
learned_variables = OrderedDict()

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
    else:
        learned_variables[variable] = value
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

def backtrack(current):
    for rule in rules:
        if rule[1]==current:
            if evaluate( parse(rule[0]), facts):
                return True
            else:

                backtrack()




def why(line):
    pass


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
