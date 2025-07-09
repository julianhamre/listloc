import unittest
import os
from snippet_extractor import SnippetExtractor

class TestSnippetExtractor(unittest.TestCase):
    __EXAMPLE_CODE_FILE_NAME = "temp_code.py"
    __EXPECTED_SNIPPET_STRINGS = {"import.txt": "import os",
                                  "greet.txt": "def greet(name):\n    print(f'Hello, {name}!')\n\ngreet('Alice')",
                                  "farewell.txt": "def farewell(name):\n    print(f'Goodbye, {name}.')\n\nfarewell('Bob')"
}
    __EXAMPLE_CODE = """# Some setup code

# BEGIN SNIPPET import
import os
# END SNIPPET


# BEGIN SNIPPET greet

def greet(name):
    print(f'Hello, {name}!')

greet('Alice')

# END SNIPPET


# Some unrelated code
print('Done')


# BEGIN SNIPPET farewell
def farewell(name):
    print(f'Goodbye, {name}.')

farewell('Bob')


# END SNIPPET
"""

    @classmethod
    def setUpClass(cls):
        with open(cls.__EXAMPLE_CODE_FILE_NAME, "wt", encoding="utf-8") as f:
            f.write(cls.__EXAMPLE_CODE)
        cls.__snippet_extractor = SnippetExtractor(f"./{cls.__EXAMPLE_CODE_FILE_NAME}")
        cls.__snippet_extractor.extract_snippets()

    @classmethod
    def tearDownClass(cls):
        os.remove(cls.__EXAMPLE_CODE_FILE_NAME)
        cls.__snippet_extractor.delete_snippet_directory_if_present()

    def test_extract_from(self):
        actual_snippet_strings = self.__extract_snippet_file_contents()
        self.assertEqual(self.__EXPECTED_SNIPPET_STRINGS, actual_snippet_strings)

    def __extract_snippet_file_contents(self):
        path_to_dir = f"./{SnippetExtractor.SNIPPET_DIRECTORY_NAME}"
        snippet_files = os.listdir(path_to_dir)
        snippet_strings = {}
        for file in snippet_files:
            path_to_file = f"{path_to_dir}/{file}"
            with open(path_to_file, "rt", encoding="utf-8") as f:
                snippet_strings[file] = f.read()
        return snippet_strings

if __name__ == "__main__":
    unittest.main()