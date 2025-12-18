import os
import tempfile
from src.listloc.extractor.listing_constants import ListingConstants

class FileCreationTools:

    def __init__(self, base_dir, subdirs, files):
        self.__BASE_DIR = base_dir
        self.__SUBDIRS = subdirs
        self.__FILES = files

    def create_subdirs_and_code_files(self):
        for dir in self.__SUBDIRS:
            os.mkdir(os.path.join(self.__BASE_DIR, dir))
        listing_strings_by_filename = self.__listing_string_dict()
        for file, listing_strings in listing_strings_by_filename.items():
            self.__write_listing_strings(file, listing_strings)

    def __listing_string_dict(self):
        listing_dict = {}
        for file in self.__FILES:
            full_file_path = os.path.join(self.__BASE_DIR, file)
            listing_names = self.__FILES[file]
            listing_dict[full_file_path] = self.__create_listing_strings(listing_names)
        return listing_dict   

    def __create_listing_strings(self, listing_names):
        listing_strings = []
        if not isinstance(listing_names, list):
            listing_names = [listing_names]
        for listing_name in listing_names:
            listing_strings.append(self.__listing_string(listing_name))
        return listing_strings
    
    @staticmethod
    def __listing_string(listing_name):
        return f"BEGIN LISTING {listing_name}\nThis is a code listing\nEND LISTING\n"
    
    def __write_listing_strings(self, file, listing_strings):
        with open(file, "wt", encoding="utf-8") as f:
            for listing_string in listing_strings:
                f.write(listing_string)  