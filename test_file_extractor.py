import unittest
import os
from file_extractor import FileExtractor

class TestFileExtractor(unittest.TestCase):
    __EXAMPLE_CODE_FILE_NAME = "temp_code.py"
    __EXPECTED_LISTING_STRINGS = {"import.txt": "import os",
                                  "greet.txt": "def greet(name):\n    print(f'Hello, {name}!')\n\ngreet('Alice')",
                                  "farewell.txt": "def farewell(name):\n    print(f'Goodbye, {name}.')\n\nfarewell('Bob')"
}
    __EXAMPLE_CODE = """# Some setup code

# BEGIN LISTING import
import os
# END LISTING


# BEGIN LISTING greet

def greet(name):
    print(f'Hello, {name}!')

greet('Alice')

# END LISTING


# Some unrelated code
print('Done')


# BEGIN LISTING farewell
def farewell(name):
    print(f'Goodbye, {name}.')

farewell('Bob')


# END LISTING
"""

    @classmethod
    def setUpClass(cls):
        with open(cls.__EXAMPLE_CODE_FILE_NAME, "wt", encoding="utf-8") as f:
            f.write(cls.__EXAMPLE_CODE)
        cls.__listing_extractor = FileExtractor(f"./{cls.__EXAMPLE_CODE_FILE_NAME}")
        cls.__listing_extractor.extract_listings()

    @classmethod
    def tearDownClass(cls):
        os.remove(cls.__EXAMPLE_CODE_FILE_NAME)
        cls.__listing_extractor.delete_listing_directory_if_present()

    def test_extract_listings(self):
        actual_listing_strings = self.__extract_listing_file_contents()
        self.assertEqual(self.__EXPECTED_LISTING_STRINGS, actual_listing_strings)

    def __extract_listing_file_contents(self):
        path_to_dir = f"./{FileExtractor.LISTING_DIRECTORY_NAME}"
        listing_files = os.listdir(path_to_dir)
        listing_strings = {}
        for file in listing_files:
            path_to_file = f"{path_to_dir}/{file}"
            with open(path_to_file, "rt", encoding="utf-8") as f:
                listing_strings[file] = f.read()
        return listing_strings

if __name__ == "__main__":
    unittest.main()