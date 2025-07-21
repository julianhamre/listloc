import unittest
import os
import tempfile
from src.listloc.extractor.file_extractor import FileExtractor

class TestFileExtractor(unittest.TestCase):
    __EXPECTED_LISTING_STRINGS = {
        f"import{FileExtractor.LISTING_FILE_EXTENSION}": "import os",
        f"greet{FileExtractor.LISTING_FILE_EXTENSION}": "def greet(name):\n    print(f'Hello, {name}!')\n\ngreet('Alice')",
        f"farewell{FileExtractor.LISTING_FILE_EXTENSION}": "def farewell(name):\n    print(f'Goodbye, {name}.')\n\nfarewell('Bob')"
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
        cls.__temp_dir = tempfile.TemporaryDirectory()
        cls.__example_code_path = os.path.join(cls.__temp_dir.name, "temp_code.py")
        cls.__listing_extractor = FileExtractor(cls.__example_code_path)

    @classmethod
    def tearDownClass(cls):
        cls.__listing_extractor.delete_listing_directory_if_present()
        cls.__temp_dir.cleanup()

    def test_extract_listings(self):
        self.assertFalse(self.__listing_extractor.extract_listings())
        self.__create_example_code_file()
        self.assertTrue(self.__listing_extractor.extract_listings())
        actual_listing_strings = self.__extract_listing_file_contents()
        self.assertEqual(self.__EXPECTED_LISTING_STRINGS, actual_listing_strings)

    def __create_example_code_file(self):
        with open(self.__example_code_path, "wt", encoding="utf-8") as f:
            f.write(self.__EXAMPLE_CODE)

    def __extract_listing_file_contents(self):
        path_to_dir = os.path.join(self.__temp_dir.name, FileExtractor.LISTING_DIRECTORY_NAME)
        listing_files = os.listdir(path_to_dir)
        listing_strings = {}
        for file in listing_files:
            path_to_file = os.path.join(path_to_dir, file)
            with open(path_to_file, "rt", encoding="utf-8") as f:
                listing_strings[file] = f.read()
        return listing_strings

if __name__ == "__main__":
    unittest.main()