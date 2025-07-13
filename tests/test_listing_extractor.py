import unittest
import os
import shutil
from extractor.listing_extractor import ListingExtractor
from extractor.file_extractor import FileExtractor

class TestListingExtractor(unittest.TestCase):

    __BASE_DIRECTORY_PATH = "./temp_dir"
    __SUBDIRS = ["dir1", "dir1/dir2", "dir1/dir3", "dir1/dir3/dir4"]
    __FILES = ["file1", "dir1/file1", "dir1/dir2/file1", "dir1/dir2/file2", "dir1/dir3/dir4/file1", "dir1/dir3/dir4/file2"]

    @classmethod
    def setUpClass(cls):
        cls.__LISTINGS = cls.__create_listing_string_dict()
        os.mkdir(cls.__BASE_DIRECTORY_PATH)
        for dir in cls.__SUBDIRS:
            os.mkdir(f"{cls.__BASE_DIRECTORY_PATH}/{dir}")
        for file, listing_string in cls.__LISTINGS.items():
            file_path = f"{cls.__BASE_DIRECTORY_PATH}/{file}"
            with open(file_path, "wt", encoding="utf-8") as f:
                f.write(listing_string)
        unclean_listing_directory = f"{cls.__BASE_DIRECTORY_PATH}/dir1/dir2/{FileExtractor.LISTING_DIRECTORY_NAME}"
        os.mkdir(unclean_listing_directory)
        with open(f"{unclean_listing_directory}/something_else.txt", "wt") as f:
            f.write("Not a listing")
    
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
    def tearDownClass(cls):
        shutil.rmtree(f"./{cls.__BASE_DIRECTORY_PATH}")

    def test_extract_all_listings(self):
        listing_extractor = ListingExtractor(f"./{self.__BASE_DIRECTORY_PATH}")
        listing_extractor.extract_all_listings()
        for file_path in self.__listing_files_that_should_exist():
            self.assertTrue(os.path.exists(file_path))
        self.assertFalse(os.path.isdir(f"{self.__BASE_DIRECTORY_PATH}/dir1/dir3/{FileExtractor.LISTING_DIRECTORY_NAME}"))

    def __listing_files_that_should_exist(self):
        paths = [f"{self.__BASE_DIRECTORY_PATH}/{FileExtractor.LISTING_DIRECTORY_NAME}/file1_listing{FileExtractor.LISTING_FILE_EXTENSION}",
                 f"{self.__BASE_DIRECTORY_PATH}/dir1/{FileExtractor.LISTING_DIRECTORY_NAME}/file1_listing{FileExtractor.LISTING_FILE_EXTENSION}",
                 f"{self.__BASE_DIRECTORY_PATH}/dir1/dir2/{FileExtractor.LISTING_DIRECTORY_NAME}/file1_listing{FileExtractor.LISTING_FILE_EXTENSION}",
                 f"{self.__BASE_DIRECTORY_PATH}/dir1/dir2/{FileExtractor.LISTING_DIRECTORY_NAME}/file2_listing{FileExtractor.LISTING_FILE_EXTENSION}",
                 f"{self.__BASE_DIRECTORY_PATH}/dir1/dir3/dir4/{FileExtractor.LISTING_DIRECTORY_NAME}/file1_listing{FileExtractor.LISTING_FILE_EXTENSION}",
                 f"{self.__BASE_DIRECTORY_PATH}/dir1/dir3/dir4/{FileExtractor.LISTING_DIRECTORY_NAME}/file2_listing{FileExtractor.LISTING_FILE_EXTENSION}"
                 ]
        return paths
    
    def test_clear_all_listing_extractions(self):
        listing_extractor = ListingExtractor(f"./{self.__BASE_DIRECTORY_PATH}")
        listing_extractor.clear_all_listing_extractions()
        for file_path in self.__listing_files_that_should_exist():
            self.assertFalse(os.path.exists(file_path))
        for directory_path in self.__listing_directories_that_should_have_been_deleted():
            self.assertFalse(os.path.isdir(directory_path))
        self.assertTrue(os.path.exists(f"{self.__BASE_DIRECTORY_PATH}/dir1/dir2/{FileExtractor.LISTING_DIRECTORY_NAME}/something_else.txt"))
        for file in self.__FILES:
            self.assertTrue(os.path.exists(f"{self.__BASE_DIRECTORY_PATH}/{file}"))
    
    def __listing_directories_that_should_have_been_deleted(self):
        paths = [f"{self.__BASE_DIRECTORY_PATH}/{FileExtractor.LISTING_DIRECTORY_NAME}",
                 f"{self.__BASE_DIRECTORY_PATH}/dir1/{FileExtractor.LISTING_DIRECTORY_NAME}",
                 f"{self.__BASE_DIRECTORY_PATH}/dir1/dir3/dir4/{FileExtractor.LISTING_DIRECTORY_NAME}",
                 ]
        return paths

    
if __name__ == "__main__":
    unittest.main()