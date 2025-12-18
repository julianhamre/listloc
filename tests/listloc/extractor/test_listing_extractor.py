import unittest
import os
from src.listloc.extractor.listing_extractor import ListingExtractor, FileExtractor
from src.listloc.extractor.listing_constants import ListingConstants
from tests.listloc.extractor.file_creation_tools import FileCreationTools
from listloc.extractor.context.extractor_context import ExtractorContext
import tempfile

class TestListingExtractor(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self._BASE_DIRECTORY_PATH = self.temp_dir.name
        self.__SUBDIRS = ["dir1", 
                          os.path.join("dir1", "dir2"), 
                          os.path.join("dir1", "dir3"), 
                          os.path.join("dir1", "dir3", "dir4")]
        self.__FILES = {"file1": "file1_listing", 
                        os.path.join("dir1", "file11"): "file11_listing", 
                        os.path.join("dir1", "dir2", "file21"): "file21_listing", 
                        os.path.join("dir1", "dir2", "file22"): "file22_listing", 
                        os.path.join("dir1", "dir3", "dir4", "file41"): "file41_listing", 
                        os.path.join("dir1", "dir3", "dir4", "file2"): "file42_listing"}
        self.__file_creator = FileCreationTools(self._BASE_DIRECTORY_PATH, self.__SUBDIRS, self.__FILES)
        self.__create_test_file_structure()
        self.__context = ExtractorContext(self._BASE_DIRECTORY_PATH)
        self.__listing_extractor = ListingExtractor(self._BASE_DIRECTORY_PATH, self.__context)
    
    def __create_test_file_structure(self):
        self.__file_creator.create_subdirs_and_code_files()
        self.__create_listing_dir_containing_non_listing_file()

    def __create_listing_dir_containing_non_listing_file(self):
        unclean_listing_directory = os.path.join(self._BASE_DIRECTORY_PATH, "dir1", "dir2", ListingConstants.LISTING_DIRECTORY_NAME)
        os.mkdir(unclean_listing_directory)
        with open(os.path.join(unclean_listing_directory, "not_a_listing.txt"), "wt") as f:
            f.write("Not a listing")

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_invalid_path(self):
        invalid_paths = [os.path.join(self._BASE_DIRECTORY_PATH, "file1"),
                         os.path.join(self._BASE_DIRECTORY_PATH, "not_a_file_or_dir"),
                         os.path.join(self._BASE_DIRECTORY_PATH, "dir1", "dir2", "file1")]
        for path in invalid_paths:
            self.assertRaises(NotADirectoryError, ListingExtractor, *(path, self.__context))
    
    def _assert_extracted_listings(self, extract_paths, global_dir=True):
        extractor = ListingExtractor(self._BASE_DIRECTORY_PATH, 
                                     self.__context,
                                     global_listing_directory=global_dir)
        extractor.extract_all_listings()
        for file_path in extract_paths:
            self.assertTrue(os.path.exists(file_path))
        listing_directory_in_empty_dir = os.path.join(self._BASE_DIRECTORY_PATH, "dir1", "dir3", ListingConstants.LISTING_DIRECTORY_NAME)
        self.assertFalse(os.path.isdir(listing_directory_in_empty_dir))

    def _assert_clear_all_listing_extractions(self, extract_paths):
        self.__listing_extractor.extract_all_listings()
        self.__listing_extractor.clear_all_listing_extractions()
        for file_path in extract_paths:
            self.assertFalse(os.path.exists(file_path))
        for directory_path in self.__listing_directories_that_should_be_deleted_after_clearing():
            self.assertFalse(os.path.isdir(directory_path))
        non_listing_file_in_listing_dir = os.path.join(self._BASE_DIRECTORY_PATH, "dir1", "dir2", ListingConstants.LISTING_DIRECTORY_NAME, "not_a_listing.txt")
        self.assertTrue(os.path.exists(non_listing_file_in_listing_dir))
        for file in self.__FILES:
            self.assertTrue(os.path.exists(os.path.join(self._BASE_DIRECTORY_PATH, file)))

    def __listing_directories_that_should_be_deleted_after_clearing(self):
        LISTING_DIRECTORIES_THAT_SHOULD_BE_DELETED = [
            os.path.join(self._BASE_DIRECTORY_PATH, ListingConstants.LISTING_DIRECTORY_NAME),
            os.path.join(self._BASE_DIRECTORY_PATH, "dir1", ListingConstants.LISTING_DIRECTORY_NAME),
            os.path.join(self._BASE_DIRECTORY_PATH, "dir1", "dir3", "dir4", ListingConstants.LISTING_DIRECTORY_NAME),
            ]
        return LISTING_DIRECTORIES_THAT_SHOULD_BE_DELETED
    
if __name__ == "__main__":
    unittest.main()