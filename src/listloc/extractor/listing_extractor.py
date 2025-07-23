import os
import shutil
from listloc.extractor.file_extractor import FileExtractor


class ListingExtractor:

    def __init__(self, base_directory_path):
        self.__validate_directory_path(base_directory_path)
        self.__base_directory_path = base_directory_path

    def __validate_directory_path(self, path):
        if not os.path.isdir(path):
            raise NotADirectoryError(f"Expected a directory path, but got: '{path}'")

    def extract_all_listings(self):
        file_paths = self.__all_file_paths()
        any_listing_extracted = False
        for path in file_paths:
            file_extractor = FileExtractor(path)
            listing_extracted = file_extractor.extract_listings()
            if not any_listing_extracted and listing_extracted:
                any_listing_extracted = True
        return any_listing_extracted
    
    def __all_file_paths(self):
        file_paths = []
        for root, dirs, files in os.walk(self.__base_directory_path):
            for file in files:
                file_paths.append(os.path.join(root, file))
        return file_paths
    
    def clear_all_listing_extractions(self):
        directory_paths = self.__all_directory_paths()
        any_listing_file_or_dir_deleted = False
        for directory in directory_paths:
            if not self.__is_listing_directory(directory):
                continue
            if self.__only_contains_listing_files(directory):
                shutil.rmtree(directory)
                any_listing_file_or_dir_deleted = True
                continue
            listing_file_deleted = self.__delete_listing_files_in(directory)
            if not any_listing_file_or_dir_deleted and listing_file_deleted:
                any_listing_file_or_dir_deleted = True
        return any_listing_file_or_dir_deleted

    def __all_directory_paths(self):
        directory_paths = []
        for root, dirs, files in os.walk(self.__base_directory_path):
            for dir in dirs:
                directory_paths.append(os.path.join(root, dir))
        return directory_paths
    
    def __is_listing_directory(self, directory):
        directory_name = os.path.basename(directory)
        return directory_name == FileExtractor.LISTING_DIRECTORY_NAME

    def __only_contains_listing_files(self, directory_path):
        files = self.__files_in_directory(directory_path)
        for file in files:
            if not self.__is_listing_file(file):
                return False
        return True
    
    def __delete_listing_files_in(self, directory_path):
        listing_file_deleted = False
        for file in self.__files_in_directory(directory_path):
            if self.__is_listing_file(file):
                os.remove(os.path.join(directory_path, file))
                listing_file_deleted = True
        return listing_file_deleted
    
    def __files_in_directory(self, directory_path):
        return os.listdir(directory_path)

    def __is_listing_file(self, file):
        return file.endswith(FileExtractor.LISTING_FILE_EXTENSION)
