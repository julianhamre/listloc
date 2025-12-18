import unittest
import os
from tests.listloc.extractor.test_listing_extractor import TestListingExtractor
from src.listloc.extractor.listing_extractor import ListingExtractor, FileExtractor
from src.listloc.extractor.listing_constants import ListingConstants
from listloc.extractor.context.action_logger import ActionLogger
import tempfile

class TestListingExtractorGlobalDir(TestListingExtractor):
    
    def setUp(self):
        super().setUp()
        self.__extract_paths = [
            os.path.join(self._BASE_DIRECTORY_PATH, ListingConstants.LISTING_DIRECTORY_NAME, f"file1_listing{ListingConstants.LISTING_FILE_EXTENSION}"),
            os.path.join(self._BASE_DIRECTORY_PATH, ListingConstants.LISTING_DIRECTORY_NAME, f"file11_listing{ListingConstants.LISTING_FILE_EXTENSION}"),
            os.path.join(self._BASE_DIRECTORY_PATH, ListingConstants.LISTING_DIRECTORY_NAME, f"file21_listing{ListingConstants.LISTING_FILE_EXTENSION}"),
            os.path.join(self._BASE_DIRECTORY_PATH, ListingConstants.LISTING_DIRECTORY_NAME, f"file22_listing{ListingConstants.LISTING_FILE_EXTENSION}"),
            os.path.join(self._BASE_DIRECTORY_PATH, ListingConstants.LISTING_DIRECTORY_NAME, f"file41_listing{ListingConstants.LISTING_FILE_EXTENSION}"),
            os.path.join(self._BASE_DIRECTORY_PATH, ListingConstants.LISTING_DIRECTORY_NAME, f"file42_listing{ListingConstants.LISTING_FILE_EXTENSION}")
            ]

    def test_extract_all_listings_to_local_dirs(self):
        self._assert_extracted_listings(self.__extract_paths, global_dir=True)

    def test_clear_all_listing_extractions(self):
        self._assert_clear_all_listing_extractions(self.__extract_paths)