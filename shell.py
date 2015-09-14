from collections import OrderedDict

root_variables = OrderedDict()
learned_variables = OrderedDict()

facts = {}
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



def learn(line):
    # apply forward chaining to create new facts
    for rule in rules:
        if eval(rule[0]):
            learned_variables[rule[1]] = True


def query(line):
    pass
def why(line):
    pass

if __name__=='__main__':
    while True:
        try:
            line = raw_input('')
            command = line.split(' ')[0].lower()
            if 'teach' == command:
                teach(line)
            elif 'learn' == command:
                learn(line)
            elif 'list' == command:
                list()
            elif 'query' == command:
                query(line)
            elif 'why' == command:
                why(line)
            else:
                break
        except:
            break


#todo: make sure you check if user input is 'False', 'True'...



"12345" -> [1,2,3,4,5]

"23242526" -> [23,24,25,26]

"12345" -> 1, 5 -> [1,2,3,4,5] 1 + len(string)


"123456719 123456720"
