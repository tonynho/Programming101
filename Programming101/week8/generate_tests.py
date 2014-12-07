
class TestsGenerator:
    def __init__(self, dsl_file_name):
        self.dsl_file_name = dsl_file_name
        self.dsl_text = self._read_file(dsl_file_name)

    def compose(self, f, g):
        return lambda x: f(g(x))

    def compose_all(self, functions):
        result = self.compose(functions[0], functions[1])
        functions = functions[2:]

        for f in functions:
            functions = self.compose(result, f)     # reads funcitons from right to left

        return result

    def _read_file(self, file_name):
        contents = ""
        with open(file_name) as read_file:
            contents = read_file.readlines()
        return contents

    def _write_file(self, file_name, text):
        with open(file_name) as write_file:
            write_file.write(text)

    def generate_file_name(self):
        self.dsl_file_name.split("_")
        # work in progress

    def write_tests(self):
        template = "teststests tests"
        file_name = self.generate_file_name()
        self._write_file(file_name, template)
"""
import unittest

{imports}

class {class_name}(unittest.TestCase):
    \"\"\"{test_doc}\"\"\"

    {test_cases}

if __name__ == '__main__':
    unittest.main()


    def testCase1(self):
        self.assertTrue(is_prime(7), "7 should noot be prime")

    def testCase2(self):
        self.assertFalse(is_prime(8), "8 should be prime")

"""


def main():
    pass


if __name__ == '__main__':
    main()