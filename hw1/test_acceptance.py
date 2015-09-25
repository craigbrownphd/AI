from unittest import TestCase
import shlex, subprocess
class TestAcceptance(TestCase):

    def create_file_with_contents(self, contents):
        mystr = ""
        for line in contents:
            mystr += line + '\n'
        filename='/home/himanshu/AI/tests/TEST_FILE.TXT'
        f = open(filename,'w')
        f.write(mystr)
        f.close()

        # args = shlex.split('echo {mystr} > {filename}'.format(
        #     mystr=mystr,
        #
        # ))
        # p = subprocess.Popen(args)
        # assert p.stderr is None

    def run_code(self):
        args = shlex.split('python shell.py')

        myinput = open('./tests/TEST_FILE.TXT')
        myoutput = open('./tests/TEST_OUTPUT.TXT', 'w')
        p = subprocess.Popen(args, stdin=myinput, stdout=myoutput, stderr=myoutput)
        p.wait()
        myoutput.flush()
        myinput.close()
        myoutput.close()
        assert p.stderr is None

    def assert_code_failed(self):
        myoutput = open('./tests/TEST_OUTPUT.TXT', 'r').read(9999)
        self.assertEqual(myoutput[0:9], 'Traceback')



        # print(open('./tests/TEST_OUTPUT.TXT', 'r').read(9999))

    def outputEquals(self, expected):
        actual = open('./tests/TEST_OUTPUT.TXT', 'r').read(9999)
        self.assertEqual(expected.strip(), actual.strip())


    def test_general(self):
        self.create_file_with_contents([
            "Teach -R a = \"some value\"",
            "Teach -L b = \"some value1\"",
            "Teach a = true",
            "Teach a -> b",
            "Learn",
            "List"
        ])
        self.run_code()
        self.outputEquals(
"""
Root Variables:
	a = "some value"
Learned Variables:
	b = "some value1"
Facts:
	a
	b
Rules:
	a -> b
"""
        )



    def test_query(self):
        self.create_file_with_contents([
            "Teach -R a = \"some value\"",
            "Teach -L b = \"some value1\"",
            "Teach a = true",
            "Teach a -> b",
            "List",
            "Query a",
            "Query b",
            "Query a&b",
            "Query a&(!b)",
            "List"
        ])
        self.run_code()
        self.outputEquals(
"""
Root Variables:
\ta = "some value"
Learned Variables:
\tb = "some value1"
Facts:
\ta
Rules:
\ta -> b
true
true
true
false
Root Variables:
\ta = "some value"
Learned Variables:
\tb = "some value1"
Facts:
\ta
Rules:
\ta -> b
"""
        )


    def test_teach_string_has_spaces(self):
        self.create_file_with_contents([
            "Teach -R a = \"space in the middle\"",
            "List"
        ])
        self.run_code()
        self.outputEquals(
"""
Root Variables:
\ta = "space in the middle"
Learned Variables:
Facts:
Rules:
"""
        )
    def test_teach_new_value_is_false(self):
        self.create_file_with_contents([
            "Teach -R a = \"a\"",
            "List"
        ])
        self.run_code()
        self.outputEquals(
"""
Root Variables:
\ta = "a"
Learned Variables:
Facts:
Rules:
"""
        )

    def test_teach_variable_cannot_be_used_twice(self):
        self.create_file_with_contents([
            "Teach -R a = \"a\"",
            "Teach -R a = \"some other value\"",
            "List"
        ])
        self.run_code()
        self.outputEquals(
"""
Root Variables:
\ta = "a"
Learned Variables:
Facts:
Rules:
"""
        )

    def test_teach_variable_possible_chars(self):
        upper_alphabet = ''.join(map(chr, range(65, 91)))
        lower_alphabet = ''.join(map(chr, range(97, 123)))

        cases = [
            upper_alphabet + '_' + lower_alphabet,
            lower_alphabet + '_' + upper_alphabet,
            '_',
            '_'+upper_alphabet,
            '_'+lower_alphabet,
            upper_alphabet+'_',
            lower_alphabet+'_',
            upper_alphabet+upper_alphabet+upper_alphabet,
            lower_alphabet+lower_alphabet+lower_alphabet+'_'

        ]
        for case in cases:
            self.create_file_with_contents([
                "Teach -R a = \"{}\"".format(case),
                "List"
            ])
            self.run_code()
            self.outputEquals(
                "Root Variables:\n\ta = \"{}\"\nLearned Variables:\nFacts:\nRules:".format(case)
            )

    def test_teach_variable_true_false_name(self):
        cases = [
            'true',
            'True',
            'TRUE',
            'tRuE',
            'false',
            'FALSE',
            'False',
            'FaLsE'
        ]
        for case in cases:
            self.create_file_with_contents([
                "Teach -R a = \"{}\"".format(case),
                "List"
            ])
            self.run_code()
            self.outputEquals(
                "Root Variables:\n\ta = \"{}\"\nLearned Variables:\nFacts:\nRules:".format(case)
            )

    def test_teach_true(self):
        self.create_file_with_contents([
            "Teach -R a = \"a\"",
            "Teach a = true",
            "List"
        ])
        self.run_code()
        self.outputEquals(
            "Root Variables:\n\ta = \"a\"\nLearned Variables:\nFacts:\n\ta\nRules:"
        )

    def test_teach_false(self):
        self.create_file_with_contents([
            "Teach -R a = \"a\"",
            "Teach a = false",
            "List"
        ])
        self.run_code()
        self.outputEquals(
            "Root Variables:\n\ta = \"a\"\nLearned Variables:\nFacts:\nRules:"
        )

    def test_throw_error_if_user_teachs_learned_variable(self):
        self.create_file_with_contents([
            "Teach -L a = \"a\"",
            "Teach a = false",
        ])
        self.run_code()
        self.assert_code_failed()


    def test_teach_variable_basic(self):
        self.create_file_with_contents([
            "Teach -R a = \"a\"",
            "Teach -L b = \"b\"",
            "Teach a -> b",
            "List",
            "Query b"
        ])
        self.run_code()
        self.outputEquals(
            "Root Variables:\n\ta = \"a\"\nLearned Variables:\n\tb = \"b\"\nFacts:\nRules:\n\ta -> b\nfalse"
        )

    def test_teach_resets_all_derived_variables_when_root_is_made_false(self):
        self.create_file_with_contents([
            "Teach -R a = \"a\"",
            "Teach -L b = \"b\"",
            "Teach -L c = \"c\"",
            "Teach a = true",
            "Teach a -> b",
            "Teach a -> c",
            "Learn",
            "Query a",
            "Query b",
            "Query c",
            "Teach a = false",
            #note: don't need to learn
            "Query a",
            "Query b",
            "Query c"
        ])
        self.run_code()
        self.outputEquals(
            "true\ntrue\ntrue\nfalse\nfalse\nfalse"
        )

    def test_teach_resets_all_derived_variables_when_root_is_made_true(self):
        self.create_file_with_contents([
            "Teach -R a = \"a\"",
            "Teach -L b = \"b\"",
            "Teach -L c = \"c\"",
            "Teach a = true",
            "Teach a -> b",
            "Teach a -> c",
            "Learn",
            "List",
            "Teach a = true",
            #note: don't need to learn
            "List"
        ])
        self.run_code()
        learn_one = "Root Variables:\n\ta = \"a\"\nLearned Variables:\n\tb = \"b\"\n\tc = \"c\"\nFacts:\n\ta\n\tb\n\tc\nRules:\n\ta -> b\n\ta -> c"
        learn_two = "Root Variables:\n\ta = \"a\"\nLearned Variables:\n\tb = \"b\"\n\tc = \"c\"\nFacts:\n\ta\nRules:\n\ta -> b\n\ta -> c"
        self.outputEquals(
            learn_one + '\n' + learn_two
        )

    def test_teach_with_and_or_not(self):
        self.create_file_with_contents([
            "Teach -R a = \"a\"",
            "Teach -L b = \"b\"",
            "Teach (a|(!(a&a))|a&a|a) -> b",
            "Learn",
            "List",
        ])
        self.run_code()
        self.outputEquals(
            'Root Variables:\n\ta = \"a\"\nLearned Variables:\n\tb = \"b\"\nFacts:\nRules:\n\t(a|(!(a&a))|a&a|a) -> b'
        )


    def test_teach_parenthesized(self):
        self.create_file_with_contents([
            "Teach -R a = \"a\"",
            "Teach -L b = \"b\"",
            "Teach (a) -> b",
            "Learn",
            "List",
        ])
        self.run_code()
        self.outputEquals(
            'Root Variables:\n\ta = \"a\"\nLearned Variables:\n\tb = \"b\"\nFacts:\nRules:\n\t(a) -> b'
        )

    def test_teach_unparenthesized(self):
        self.create_file_with_contents([
            "Teach -R a = \"a\"",
            "Teach -L b = \"b\"",
            "Teach a -> b",
            "Learn",
            "List",
        ])
        self.run_code()
        self.outputEquals(
            'Root Variables:\n\ta = \"a\"\nLearned Variables:\n\tb = \"b\"\nFacts:\nRules:\n\ta -> b'
        )


    def test_invalid_input(self):
        self.create_file_with_contents([
            "Teach -R a = \"a\"",
            "Teach -L b = \"b\"",
            "teach (a|(!(a&a))|a&a|a) -> b",
            "Learn",
            "List",
        ])
        self.run_code()
        self.outputEquals(
            'Root Variables:\n\ta = \"a\"\nLearned Variables:\n\tb = \"b\"\nFacts:\nRules:\n'
        )

    def test_list_facts_variables_rules_in_order(self):
        self.create_file_with_contents([
            "Teach -R a = \"a\"",
            "Teach -L b = \"b\"",
            "Teach -R c = \"c\"",
            "Teach -L d = \"d\"",
            "Teach -R e = \"e\"",
            "Teach -L f = \"f\"",
            "Teach c -> d",
            "Teach a -> b",
            "Teach e -> f",
            "Teach a = true",
            "Teach c = true",
            "Teach e = true",
            "Learn",
            "List"
        ])
        self.run_code()
        self.outputEquals(
            'Root Variables:\n\ta = \"a\"\n\tc = \"c\"\n\te = \"e\"\nLearned Variables:\n\tb = \"b\"\n\td = \"d\"\n\tf = \"f\"\nFacts:\n\ta\n\tb\n\tc\n\td\n\te\n\tf\nRules:\n\tc -> d\n\ta -> b\n\te -> f'
        )

    #todo: we need to ignore invalid input. THIS INCLUDES INCORRRECT CASE!!!!!

    def test_possible_incorrect_sequence(self):
        self.create_file_with_contents([
            "Teach -L a = \"a\"",
            "Teach -R b = \"b\"",
            "Teach b -> a",
            "Learn",
            "Query a",
            "Query b",
            "Teach b = true",
            "Query b",
            "Query a",
        ])
        self.run_code()
        self.outputEquals(
            'false\nfalse\ntrue\ntrue'
        )

