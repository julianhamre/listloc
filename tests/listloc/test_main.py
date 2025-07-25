import unittest
import tempfile
import os
from typer.testing import CliRunner
from listloc.main import app, get_version_from_toml
from listloc.extractor.listing_constants import ListingConstants

runner = CliRunner()

class TestCLI(unittest.TestCase):
    def setUp(self):
        self.__temp_dir = tempfile.TemporaryDirectory()
        self.__BASE_DIRECTORY_PATH = self.__temp_dir.name
        self.__STALE_LISTING_FILE_PATH = os.path.join(self.__BASE_DIRECTORY_PATH, ListingConstants.LISTING_DIRECTORY_NAME, f"outdated{ListingConstants.LISTING_FILE_EXTENSION}")

    def tearDown(self):
        self.__temp_dir.cleanup()

    def test_version_option(self):
        expected_version = get_version_from_toml()
        self.__is_semver_string(expected_version)
        result = runner.invoke(app, ["--version"])
        self.assertEqual(expected_version, result.output.strip())

    def __is_semver_string(self, version: str):
        semver_pattern = "^(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$"
        self.assertRegex(version.strip(), semver_pattern)

    def test_extract_no_listings(self):
        result = runner.invoke(app, ["extract", self.__BASE_DIRECTORY_PATH])
        self.assertEqual(f"No listings to extract from \n'{self.__BASE_DIRECTORY_PATH}'\n", result.output)

    def test_extract_no_listings_with_prune_option(self):
        result = runner.invoke(app, ["extract", "--prune", self.__BASE_DIRECTORY_PATH])
        self.assertEqual(f"No listings to extract from \n'{self.__BASE_DIRECTORY_PATH}'\n", result.output)

    def test_extract_listing(self):
        self.__write_source_file_with_listing()
        result = runner.invoke(app, ["extract", self.__BASE_DIRECTORY_PATH])
        self.assertTrue(self.__listing_file_present())
        self.assertEqual(f"Extracted a total of 1 listing from 1 source file\n", result.output)

    def test_extract_with_prune_option(self):
        self.__write_source_file_with_listing()
        self.__write_stale_listing_file()
        result = runner.invoke(app, ["extract", "--prune", self.__BASE_DIRECTORY_PATH])
        self.assertTrue(self.__listing_file_present())
        self.assertFalse(os.path.exists(self.__STALE_LISTING_FILE_PATH))
        expected_output = "Deleted a total of 1 listing extraction\nExtracted a total of 1 listing from 1 source file\n"
        self.assertEqual(expected_output, result.output)

    def test_extract_with_prune_and_verbose(self):
        self.__write_source_file_with_listing()
        self.__write_stale_listing_file()
        result = runner.invoke(app, ["extract", "--prune", "--verbose", self.__BASE_DIRECTORY_PATH])
        expected_detailed_log = f"""
Deleted '{os.path.join(self.__BASE_DIRECTORY_PATH, "listings", "outdated.listing")}'
Removed '{os.path.join(self.__BASE_DIRECTORY_PATH, "listings")}'
Extracted 1 listing from '{os.path.join(self.__BASE_DIRECTORY_PATH, "example.txt")}'
Created '{os.path.join(self.__BASE_DIRECTORY_PATH, "listings")}'
Wrote '{os.path.join(self.__BASE_DIRECTORY_PATH, "listings", "foo.listing")}'"""
        self.assertIn(expected_detailed_log.replace("\n", ""), result.output.replace("\n", ""))
        expected_summary = "Deleted a total of 1 listing extraction\nExtracted a total of 1 listing from 1 source file\n"
        self.assertIn(expected_summary, result.output)

    def test_clear_no_listings(self):
        result = runner.invoke(app, ["clear", self.__BASE_DIRECTORY_PATH])
        self.assertFalse(self.__listing_file_present())
        self.assertEqual(f"Nothing to clear in \n'{self.__BASE_DIRECTORY_PATH}'\n", result.output)

    def test_clear_listings(self):
        self.__write_source_file_with_listing()
        self.__write_stale_listing_file()
        runner.invoke(app, ["extract", self.__BASE_DIRECTORY_PATH])
        result = runner.invoke(app, ["clear", self.__BASE_DIRECTORY_PATH])
        self.assertFalse(self.__listing_file_present())
        self.assertEqual(f"Deleted a total of 2 listing extractions\n", result.output)

    def test_clear_with_verbose_option(self):
        self.__write_source_file_with_listing()
        self.__write_stale_listing_file()
        runner.invoke(app, ["extract", self.__BASE_DIRECTORY_PATH])
        result = runner.invoke(app, ["clear", "--verbose", self.__BASE_DIRECTORY_PATH])
        expected_detailed_log = f"""
Deleted '{os.path.join(self.__BASE_DIRECTORY_PATH, "listings", "outdated.listing")}'
Deleted '{os.path.join(self.__BASE_DIRECTORY_PATH, "listings", "foo.listing")}'
Removed '{os.path.join(self.__BASE_DIRECTORY_PATH, "listings")}'"""
        self.assertIn(expected_detailed_log.replace("\n", ""), result.output.replace("\n", ""))


    def __listing_file_present(self):
        for root, dirs, files in os.walk(self.__BASE_DIRECTORY_PATH):
            for file in files:
                if file.endswith(ListingConstants.LISTING_FILE_EXTENSION):
                    return True
        return False

    def __write_source_file_with_listing(self):
        path = os.path.join(self.__BASE_DIRECTORY_PATH, "example.txt")
        self.__write_file(path, "BEGIN LISTING foo\nprint('hello')\nEND LISTING")
        
    def __write_stale_listing_file(self):
        listing_directory_path = os.path.join(self.__BASE_DIRECTORY_PATH, ListingConstants.LISTING_DIRECTORY_NAME)
        os.mkdir(listing_directory_path)
        self.__write_file(self.__STALE_LISTING_FILE_PATH, "outdated listing here")

    def __write_file(self, path, content):
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)