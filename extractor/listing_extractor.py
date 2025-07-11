import os
from extractor.file_extractor import FileExtractor


class ListingExtractor:

    def __init__(self, base_directory_path):
        self.__base_directory_path = base_directory_path

    def extract_all_listings(self):
        file_paths = self.__all_file_paths()
        for path in file_paths:
            file_extractor = FileExtractor(path)
            file_extractor.extract_listings()
    
    def __all_file_paths(self):
        file_paths = []
        for root, dirs, files in os.walk(self.__base_directory_path):
            for file in files:
                file_paths.append(os.path.join(root, file))
        return file_paths