import os
from listloc.extractor.file_extractor import FileExtractor
from listloc.extractor.action_logger import ActionLogger
from listloc.extractor.listing_constants import ListingConstants


class ListingExtractor:

    def __init__(self, base_directory_path, action_logger: ActionLogger):
        self.__validate_directory_path(base_directory_path)
        self.__base_directory_path = base_directory_path
        self.__logger = action_logger

    def __validate_directory_path(self, path):
        if not os.path.isdir(path):
            raise NotADirectoryError(f"Expected a directory path, but got: '{path}'")

    def extract_all_listings(self):
        file_paths = self.__all_file_paths()
        for path in file_paths:
            file_extractor = FileExtractor(path, self.__logger)
            file_extractor.extract_listings()
    
    def __all_file_paths(self):
        file_paths = []
        for root, dirs, files in os.walk(self.__base_directory_path):
            for file in files:
                file_paths.append(os.path.join(root, file))
        return file_paths
    
    def clear_all_listing_extractions(self):
        directory_paths = self.__all_directory_paths()
        for directory in directory_paths:
            self.__clear_directory(directory)

    def __all_directory_paths(self):
        directory_paths = []
        for root, dirs, files in os.walk(self.__base_directory_path):
            for dir in dirs:
                directory_paths.append(os.path.join(root, dir))
        return directory_paths
    
    def __clear_directory(self, directory_path):
        if not self.__is_listing_directory(directory_path):
            return
        self.__delete_listing_files_in(directory_path)
        if self.__directory_is_empty(directory_path):
            os.rmdir(directory_path)
            self.__logger.log_removed_directory(directory_path)
    
    def __is_listing_directory(self, directory_path):
        directory_name = os.path.basename(directory_path)
        return directory_name == ListingConstants.LISTING_DIRECTORY_NAME
    
    def __directory_is_empty(self, directory_path):
        return len(os.listdir(directory_path)) == 0
    
    def __delete_listing_files_in(self, directory_path):
        for file in self.__files_in_directory(directory_path):
            if self.__is_listing_file(file):
                file_path = os.path.join(directory_path, file)
                os.remove(file_path)
                self.__logger.log_deleted_file(file_path)
    
    def __files_in_directory(self, directory_path):
        return os.listdir(directory_path)

    def __is_listing_file(self, file):
        return file.endswith(ListingConstants.LISTING_FILE_EXTENSION)
