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
            "learn",
            "list"
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
            "list",
            "query a",
            "query b",
            "query a&b",
            "query a&(!b)",
            "list"
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
            "list"
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
            "list"
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
            "list"
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
                "list"
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
                "list"
            ])
            self.run_code()
            self.outputEquals(
                "Root Variables:\n\ta = \"{}\"\nLearned Variables:\nFacts:\nRules:".format(case)
            )

    def test_teach_true(self):
        self.create_file_with_contents([
            "Teach -R a = \"a\"",
            "Teach a = true",
            "list"
        ])
        self.run_code()
        self.outputEquals(
            "Root Variables:\n\ta = \"a\"\nLearned Variables:\nFacts:\n\ta\nRules:"
        )

    def test_teach_false(self):
        self.create_file_with_contents([
            "Teach -R a = \"a\"",
            "Teach a = false",
            "list"
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
            "list",
            "query b"
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
            "learn",
            "query a",
            "query b",
            "query c",
            "Teach a = false",
            #note: don't need to learn
            "query a",
            "query b",
            "query c"
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
            "learn",
            "list",
            "Teach a = true",
            #note: don't need to learn
            "list"
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
            "learn",
            "list",
        ])
        self.run_code()
        self.outputEquals(
            'Root Variables:\n\ta = \"a\"\nLearned Variables:\n\tb = \"b\"\nFacts:\nRules:\n\t(a|(!(a&a))|a&a|a) -> b'
        )


    #todo: we need to ignore invalid input. THIS INCLUDES INCORRRECT CASE!!!!!

    #todo: list's facts section prints out all learned variables that are true as well!!!!!!!!!!!

    #todo: this sequence is wrong?
#         Teach -L a = "a"
# Teach -R b = "b"
# Teach b -> a
# learn
# query a
# false
# query b
# false
# Teach b = true
# query b
# true
# query a
# true
