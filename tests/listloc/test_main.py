import unittest
import tempfile
import os
import shutil
from typer.testing import CliRunner
from listloc.main import app
from listloc.extractor.file_extractor import FileExtractor

runner = CliRunner()

class TestCLI(unittest.TestCase):
    def setUp(self):
        self.__temp_dir = tempfile.TemporaryDirectory()
        self.__BASE_DIRECTORY_PATH = self.__temp_dir.name
        self.__STALE_LISTING_FILE_PATH = os.path.join(self.__BASE_DIRECTORY_PATH, FileExtractor.LISTING_DIRECTORY_NAME, f"outdated{FileExtractor.LISTING_FILE_EXTENSION}")

    def tearDown(self):
        self.__temp_dir.cleanup()

    def test_extract_no_listings(self):
        result = runner.invoke(app, ["extract", self.__BASE_DIRECTORY_PATH])
        self.assertEqual(f"No listings to extract from {self.__BASE_DIRECTORY_PATH}\n", result.output)

    def test_extract_no_listings_with_prune_option(self):
        result = runner.invoke(app, ["extract", "--prune", self.__BASE_DIRECTORY_PATH])
        self.assertEqual(f"No listing files or directories to delete in {self.__BASE_DIRECTORY_PATH}\nNo listings to extract from {self.__BASE_DIRECTORY_PATH}\n", result.output)

    def test_extract_with_listing(self):
        self.__write_source_file_with_listing()
        result = runner.invoke(app, ["extract", self.__BASE_DIRECTORY_PATH])
        self.assertTrue(self.__listing_file_present())
        self.assertEqual(f"Extracted listings from {self.__BASE_DIRECTORY_PATH}\n", result.output)

    def test_extract_with_prune_option(self):
        self.__write_source_file_with_listing()
        self.__write_stale_listing_file()
        result = runner.invoke(app, ["extract", "--prune", self.__BASE_DIRECTORY_PATH])
        self.assertTrue(self.__listing_file_present())
        self.assertFalse(os.path.exists(self.__STALE_LISTING_FILE_PATH))
        expected_output = f"Deleted listings in {self.__BASE_DIRECTORY_PATH}\nExtracted listings from {self.__BASE_DIRECTORY_PATH}\n"
        self.assertEqual(expected_output, result.output)

    def test_clear_no_listings(self):
        result = runner.invoke(app, ["clear", self.__BASE_DIRECTORY_PATH])
        self.assertFalse(self.__listing_file_present())
        self.assertEqual(f"No listing files or directories to delete in {self.__BASE_DIRECTORY_PATH}\n", result.output)

    def test_clear_listings(self):
        self.__write_source_file_with_listing()
        runner.invoke(app, ["extract", self.__BASE_DIRECTORY_PATH])
        result = runner.invoke(app, ["clear", self.__BASE_DIRECTORY_PATH])
        self.assertFalse(self.__listing_file_present())
        self.assertEqual(f"Deleted listings in {self.__BASE_DIRECTORY_PATH}\n", result.output)

    def __listing_file_present(self):
        for root, dirs, files in os.walk(self.__BASE_DIRECTORY_PATH):
            for file in files:
                if file.endswith(FileExtractor.LISTING_FILE_EXTENSION):
                    return True
        return False

    def __write_source_file_with_listing(self):
        path = os.path.join(self.__BASE_DIRECTORY_PATH, "example.txt")
        self.__write_file(path, "BEGIN LISTING foo\nprint('hello')\nEND LISTING")
        
    def __write_stale_listing_file(self):
        listing_directory_path = os.path.join(self.__BASE_DIRECTORY_PATH, FileExtractor.LISTING_DIRECTORY_NAME)
        os.mkdir(listing_directory_path)
        self.__write_file(self.__STALE_LISTING_FILE_PATH, "outdated listing here")

    def __write_file(self, path, content):
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)