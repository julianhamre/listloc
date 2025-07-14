import unittest
import os
import shutil
from src.listloc.extractor.listing_extractor import ListingExtractor, FileExtractor
import time

class TestListingExtractor(unittest.TestCase):

    __BASE_DIRECTORY_PATH = os.path.join(".", "temp_dir")
    __SUBDIRS = ["dir1", os.path.join("dir1", "dir2"), os.path.join("dir1", "dir3"), os.path.join("dir1", "dir3", "dir4")]
    __FILES = ["file1", os.path.join("dir1", "file1"), os.path.join("dir1", "dir2", "file1"), os.path.join("dir1", "dir2", "file2"), os.path.join("dir1", "dir3", "dir4", "file1"), os.path.join("dir1", "dir3", "dir4", "file2")]

    __LISTING_FILES_THAT_SHOULD_BE_CREATED = [
        os.path.join(__BASE_DIRECTORY_PATH, FileExtractor.LISTING_DIRECTORY_NAME, f"file1_listing{FileExtractor.LISTING_FILE_EXTENSION}"),
        os.path.join(__BASE_DIRECTORY_PATH, "dir1", FileExtractor.LISTING_DIRECTORY_NAME, f"file1_listing{FileExtractor.LISTING_FILE_EXTENSION}"),
        os.path.join(__BASE_DIRECTORY_PATH, "dir1", "dir2", FileExtractor.LISTING_DIRECTORY_NAME, f"file1_listing{FileExtractor.LISTING_FILE_EXTENSION}"),
        os.path.join(__BASE_DIRECTORY_PATH, "dir1", "dir2", FileExtractor.LISTING_DIRECTORY_NAME, f"file2_listing{FileExtractor.LISTING_FILE_EXTENSION}"),
        os.path.join(__BASE_DIRECTORY_PATH, "dir1", "dir3", "dir4", FileExtractor.LISTING_DIRECTORY_NAME, f"file1_listing{FileExtractor.LISTING_FILE_EXTENSION}"),
        os.path.join(__BASE_DIRECTORY_PATH, "dir1", "dir3", "dir4", FileExtractor.LISTING_DIRECTORY_NAME, f"file2_listing{FileExtractor.LISTING_FILE_EXTENSION}")
        ]
    
    __LISTING_DIRECTORIES_THAT_SHOULD_BE_DELETED = [
        os.path.join(__BASE_DIRECTORY_PATH, FileExtractor.LISTING_DIRECTORY_NAME),
        os.path.join(__BASE_DIRECTORY_PATH, "dir1", FileExtractor.LISTING_DIRECTORY_NAME),
        os.path.join(__BASE_DIRECTORY_PATH, "dir1", "dir3", "dir4", FileExtractor.LISTING_DIRECTORY_NAME),
        ]

    def setUp(self):
        self.__LISTINGS_STRINGS = self.__create_listing_string_dict()
        try:
            os.mkdir(self.__BASE_DIRECTORY_PATH)
        except FileExistsError:
            pass
        self.__listing_extractor = ListingExtractor(self.__BASE_DIRECTORY_PATH)
    
    def __create_listing_string_dict(self):
        listing_dict = {}
        for file in self.__FILES:
            listing_dict[file] = self.__create_listing_string(f"{os.path.basename(file)}_listing")
        return listing_dict

    @staticmethod
    def __create_listing_string(listing_name):
        return f"BEGIN LISTING {listing_name}\nThis is a code listing\nEND LISTING"
    
    def __create_subdirs_and_code_files(self):
        for dir in self.__SUBDIRS:
            os.mkdir(os.path.join(self.__BASE_DIRECTORY_PATH, dir))
        for file, listing_string in self.__LISTINGS_STRINGS.items():
            file_path = os.path.join(self.__BASE_DIRECTORY_PATH, file)
            with open(file_path, "wt", encoding="utf-8") as f:
                f.write(listing_string)
        self.__create_listing_dir_containing_non_listing_file()

    @classmethod
    def __create_listing_dir_containing_non_listing_file(cls):
        unclean_listing_directory = os.path.join(cls.__BASE_DIRECTORY_PATH, "dir1", "dir2", FileExtractor.LISTING_DIRECTORY_NAME)
        os.mkdir(unclean_listing_directory)
        with open(os.path.join(unclean_listing_directory, "not_a_listing.txt"), "wt") as f:
            f.write("Not a listing")

    def tearDown(self):
        shutil.rmtree(self.__BASE_DIRECTORY_PATH)

    def test_extract_all_listings(self):
        self.assertFalse(self.__listing_extractor.extract_all_listings())
        self.__create_subdirs_and_code_files()
        self.assertTrue(self.__listing_extractor.extract_all_listings())
        for file_path in self.__LISTING_FILES_THAT_SHOULD_BE_CREATED:
            self.assertTrue(os.path.exists(file_path))
        listing_directory_in_empty_dir = os.path.join(self.__BASE_DIRECTORY_PATH, "dir1", "dir3", FileExtractor.LISTING_DIRECTORY_NAME)
        self.assertFalse(os.path.isdir(listing_directory_in_empty_dir))
    
    def test_clear_all_listing_extractions(self):
        self.assertFalse(self.__listing_extractor.clear_all_listing_extractions())
        self.__create_subdirs_and_code_files()
        self.__listing_extractor.extract_all_listings()
        self.assertTrue(self.__listing_extractor.clear_all_listing_extractions())
        for file_path in self.__LISTING_FILES_THAT_SHOULD_BE_CREATED:
            self.assertFalse(os.path.exists(file_path))
        for directory_path in self.__LISTING_DIRECTORIES_THAT_SHOULD_BE_DELETED:
            self.assertFalse(os.path.isdir(directory_path))
        non_listing_file_in_listing_dir = os.path.join(self.__BASE_DIRECTORY_PATH, "dir1", "dir2", FileExtractor.LISTING_DIRECTORY_NAME, "not_a_listing.txt")
        self.assertTrue(os.path.exists(non_listing_file_in_listing_dir))
        for file in self.__FILES:
            self.assertTrue(os.path.exists(os.path.join(self.__BASE_DIRECTORY_PATH, file)))

    
if __name__ == "__main__":
    unittest.main()