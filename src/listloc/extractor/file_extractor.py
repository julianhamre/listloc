import re
import os
from listloc.extractor.listing import Listing
import shutil

class FileExtractor:
    LISTING_DIRECTORY_NAME = "listings"
    LISTING_FILE_EXTENSION = ".listing"

    def __init__(self, source_file_path):
        self.__source_file_path = source_file_path
        self.__parent_directory_path = os.path.dirname(self.__source_file_path)
        self.__listing_directory_path = f"{self.__parent_directory_path}/{self.LISTING_DIRECTORY_NAME}"

    def extract_listings(self):
        """
        Extracts every valid code listing from the given source file and saves their contents 
        in their own designated files. The listing files will be stored in their own directory
        located in the directory of the code file that is extracted from. A valid listing is 
        the content in between the statements 'BEGIN LISTING <name>' and 'END LISTING'. 
        The <name> argument decides the listing file names.
        """
        if not self.__is_utf8_encoding():
            return
        with open(self.__source_file_path, "rt", encoding="utf-8") as f:
            source_code = f.read()
            pattern = f"{Listing.BEGIN_STATEMENT}.*?{Listing.END_STATEMENT}"
            listing_strings = re.findall(pattern, source_code, flags=re.DOTALL)
            listings = self.__construct_listings(listing_strings)
            self.__write_listing_files(listings)
    
    def __is_utf8_encoding(self, blocksize=512):
        try:
            with open(self.__source_file_path, 'rb') as f:
                chunk = f.read(blocksize)
            # If it decodes to UTF-8 without error, assume it's a text file
            chunk.decode('utf-8')
            return True
        except (UnicodeDecodeError, OSError):
            return False

    def __construct_listings(self, listing_strings):
        listings = []
        for listing_string in listing_strings:
            listings.append(Listing(listing_string))
        return listings
   
    def __write_listing_files(self, listings):
        if listings:
            self.__create_directory_if_absent()
        for listing in listings:
            self.__write_listing_file(listing)

    def __create_directory_if_absent(self):
        try:
            os.mkdir(self.__listing_directory_path)
        except FileExistsError:
            pass

    def __write_listing_file(self, listing):
        write_path = f"{self.__listing_directory_path}/{listing.name}{self.LISTING_FILE_EXTENSION}"
        with open(write_path, "wt", encoding="utf-8") as f:
            f.write(listing.content)

    def delete_listing_directory_if_present(self):
        if os.path.isdir(self.__listing_directory_path):
            shutil.rmtree(self.__listing_directory_path)