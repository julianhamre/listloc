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
        paths = [f"{self.__BASE_DIRECTORY_PATH}/{FileExtractor.LISTING_DIRECTORY_NAME}/file1_listing.txt",
                 f"{self.__BASE_DIRECTORY_PATH}/dir1/{FileExtractor.LISTING_DIRECTORY_NAME}/file1_listing.txt",
                 f"{self.__BASE_DIRECTORY_PATH}/dir1/dir2/{FileExtractor.LISTING_DIRECTORY_NAME}/file1_listing.txt",
                 f"{self.__BASE_DIRECTORY_PATH}/dir1/dir2/{FileExtractor.LISTING_DIRECTORY_NAME}/file2_listing.txt",
                 f"{self.__BASE_DIRECTORY_PATH}/dir1/dir3/dir4/{FileExtractor.LISTING_DIRECTORY_NAME}/file1_listing.txt",
                 f"{self.__BASE_DIRECTORY_PATH}/dir1/dir3/dir4/{FileExtractor.LISTING_DIRECTORY_NAME}/file2_listing.txt"
                 ]
        return paths
    
if __name__ == "__main__":
    unittest.main()