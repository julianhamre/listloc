import os

from tests.listloc.extractor.test_listing_extractor_tools.base_test_listing_extractor import BaseTestListingExtractor

class TestNotExtractedFromListingFile(BaseTestListingExtractor):

    def test_not_extracted_from_listing_file(self):
        files = {"file1": "listing1",
                 "file2.listing": "listing2"}
        self._create_test_file_structure([], files)
        self._listing_extractor.extract_all_listings()
        expected_extract = os.path.join(self._BASE_DIRECTORY_PATH, "listings", "listing1.listing")
        unexpected_extract = os.path.join(self._BASE_DIRECTORY_PATH, "listings", "listing2.listing")
        self.assertTrue(os.path.exists(expected_extract))
        self.assertFalse(os.path.exists(unexpected_extract))