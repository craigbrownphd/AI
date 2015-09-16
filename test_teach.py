from unittest import TestCase
import shlex, subprocess
class TestParse(TestCase):

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
        args = shlex.split('python shell.py < ./tests/TEST_FILE.TXT')
        p = subprocess.Popen(args)
        assert p.stderr is None
        print(p.stdout)
        assert False

    def test_parse_empty(self):
        self.create_file_with_contents([
            "Teach -R a = \"some value\"",
            "Teach -L b = \"some value1\"",
            "Teach a = true",
            "Teach a -> b",
            "learn",
            "list"
        ])

        self.run_code()



