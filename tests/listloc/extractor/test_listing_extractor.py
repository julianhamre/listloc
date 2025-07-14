import unittest
import os
import shutil
from src.listloc.extractor.listing_extractor import ListingExtractor, FileExtractor

class TestListingExtractor(unittest.TestCase):

    __BASE_DIRECTORY_PATH = "./temp_dir"
    __SUBDIRS = ["dir1", "dir1/dir2", "dir1/dir3", "dir1/dir3/dir4"]
    __FILES = ["file1", "dir1/file1", "dir1/dir2/file1", "dir1/dir2/file2", "dir1/dir3/dir4/file1", "dir1/dir3/dir4/file2"]

    __LISTING_FILES_THAT_SHOULD_BE_CREATED = [
        f"{__BASE_DIRECTORY_PATH}/{FileExtractor.LISTING_DIRECTORY_NAME}/file1_listing{FileExtractor.LISTING_FILE_EXTENSION}",
        f"{__BASE_DIRECTORY_PATH}/dir1/{FileExtractor.LISTING_DIRECTORY_NAME}/file1_listing{FileExtractor.LISTING_FILE_EXTENSION}",
        f"{__BASE_DIRECTORY_PATH}/dir1/dir2/{FileExtractor.LISTING_DIRECTORY_NAME}/file1_listing{FileExtractor.LISTING_FILE_EXTENSION}",
        f"{__BASE_DIRECTORY_PATH}/dir1/dir2/{FileExtractor.LISTING_DIRECTORY_NAME}/file2_listing{FileExtractor.LISTING_FILE_EXTENSION}",
        f"{__BASE_DIRECTORY_PATH}/dir1/dir3/dir4/{FileExtractor.LISTING_DIRECTORY_NAME}/file1_listing{FileExtractor.LISTING_FILE_EXTENSION}",
        f"{__BASE_DIRECTORY_PATH}/dir1/dir3/dir4/{FileExtractor.LISTING_DIRECTORY_NAME}/file2_listing{FileExtractor.LISTING_FILE_EXTENSION}"
        ]
    
    __LISTING_DIRECTORIES_THAT_SHOULD_BE_DELETED = [
        f"{__BASE_DIRECTORY_PATH}/{FileExtractor.LISTING_DIRECTORY_NAME}",
        f"{__BASE_DIRECTORY_PATH}/dir1/{FileExtractor.LISTING_DIRECTORY_NAME}",
        f"{__BASE_DIRECTORY_PATH}/dir1/dir3/dir4/{FileExtractor.LISTING_DIRECTORY_NAME}",
        ]

    @classmethod
    def setUpClass(cls):
        cls.__LISTINGS_STRINGS = cls.__create_listing_string_dict()
        os.mkdir(cls.__BASE_DIRECTORY_PATH)
        cls.__create_subdirs_and_code_files()
        cls.__create_listing_dir_containing_non_listing_file()
    
    @classmethod
    def __create_listing_string_dict(cls):
        listing_dict = {}
        for file in cls.__FILES:
            listing_dict[file] = cls.__create_listing_string(f"{os.path.basename(file)}_listing")
        return listing_dict

    @staticmethod
    def __create_listing_string(listing_name):
        return f"BEGIN LISTING {listing_name}\nThis is a code listing\nEND LISTING"
    
    @classmethod
    def __create_subdirs_and_code_files(cls):
        for dir in cls.__SUBDIRS:
            os.mkdir(f"{cls.__BASE_DIRECTORY_PATH}/{dir}")
        for file, listing_string in cls.__LISTINGS_STRINGS.items():
            file_path = f"{cls.__BASE_DIRECTORY_PATH}/{file}"
            with open(file_path, "wt", encoding="utf-8") as f:
                f.write(listing_string)

    @classmethod
    def __create_listing_dir_containing_non_listing_file(cls):
        unclean_listing_directory = f"{cls.__BASE_DIRECTORY_PATH}/dir1/dir2/{FileExtractor.LISTING_DIRECTORY_NAME}"
        os.mkdir(unclean_listing_directory)
        with open(f"{unclean_listing_directory}/not_a_listing.txt", "wt") as f:
            f.write("Not a listing")

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(f"{cls.__BASE_DIRECTORY_PATH}")

    def test_extract_all_listings(self):
        listing_extractor = ListingExtractor(f"{self.__BASE_DIRECTORY_PATH}")
        listing_extractor.extract_all_listings()
        for file_path in self.__LISTING_FILES_THAT_SHOULD_BE_CREATED:
            self.assertTrue(os.path.exists(file_path))
        listing_directory_in_empty_dir = f"{self.__BASE_DIRECTORY_PATH}/dir1/dir3/{FileExtractor.LISTING_DIRECTORY_NAME}"
        self.assertFalse(os.path.isdir(listing_directory_in_empty_dir))
    
    def test_clear_all_listing_extractions(self):
        listing_extractor = ListingExtractor(f"{self.__BASE_DIRECTORY_PATH}")
        listing_extractor.extract_all_listings()
        listing_extractor.clear_all_listing_extractions()
        for file_path in self.__LISTING_FILES_THAT_SHOULD_BE_CREATED:
            self.assertFalse(os.path.exists(file_path))
        for directory_path in self.__LISTING_DIRECTORIES_THAT_SHOULD_BE_DELETED:
            self.assertFalse(os.path.isdir(directory_path))
        non_listing_file_in_listing_dir = f"{self.__BASE_DIRECTORY_PATH}/dir1/dir2/{FileExtractor.LISTING_DIRECTORY_NAME}/not_a_listing.txt"
        self.assertTrue(os.path.exists(non_listing_file_in_listing_dir))
        for file in self.__FILES:
            self.assertTrue(os.path.exists(f"{self.__BASE_DIRECTORY_PATH}/{file}"))

    
if __name__ == "__main__":
    unittest.main()