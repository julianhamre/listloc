import unittest
import tempfile
import os
from listloc.extractor.context.extractor_context import ExtractorContext
from src.listloc.extractor.listing_extractor import ListingExtractor
from tests.listloc.extractor.file_creation_tools import FileCreationTools
from tests.listloc.extractor.base_test_listing_extractor import BaseTestListingExtractor

class TestDuplicateListingNames(BaseTestListingExtractor):

    def test_two_equal_names_in_one_file(self):
        subdirs = ["dir1"]
        file_path = os.path.join("dir1", "file11")
        listing_name = "listing1"
        files = {file_path: [listing_name, listing_name]}
        self._create_test_file_structure(subdirs, files)
        expected_message = f"""The listing name '{listing_name}' must only be used to name one listing. It is currently used:
- 2 times in '{os.path.join(self._BASE_DIRECTORY_PATH, file_path)}'"""
        self.assertRaisesRegex(Exception, expected_message, self._listing_extractor.extract_all_listings)

    def test_multiple_equal_names(self):
        file11 = os.path.join("dir1", "file11")
        file21 = os.path.join("dir1", "dir2", "file21")
        file22 = os.path.join("dir1", "dir2", "file22")
        listing_name = "listing1"
        subdirs = [os.path.dirname(file11), os.path.dirname(file21)]
        files = {file11: listing_name,
                 file21: listing_name,
                 file22: [listing_name, listing_name]}
        self._create_test_file_structure(subdirs, files)
        expected_message = f"""The listing name '{listing_name}' must only be used to name one listing. It is currently used:
- 1 time in '{os.path.join(self._BASE_DIRECTORY_PATH, file11)}'
- 1 time in '{os.path.join(self._BASE_DIRECTORY_PATH, file21)}'
- 2 times in '{os.path.join(self._BASE_DIRECTORY_PATH, file22)}'"""
        self.assertRaisesRegex(Exception, expected_message, self._listing_extractor.extract_all_listings)