import re
import os
from listloc.extractor.listing_constants import ListingConstants
from listloc.extractor.listing import Listing
from listloc.extractor.extractor_context import ExtractorContext

class FileExtractor:

    def __init__(self, source_file_path, context: ExtractorContext):
        self.__source_file_path = source_file_path
        self.__parent_directory_path = os.path.dirname(self.__source_file_path)
        self.__listing_directory_path = os.path.join(self.__parent_directory_path, ListingConstants.LISTING_DIRECTORY_NAME)
        self.__context = context

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
            self.__context.action_logger.log_extracted(self.__source_file_path, len(listings))
            self.__write_listing_files(listings)

    def __is_utf8_encoding(self, blocksize=8192):
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
            try:
                listings.append(Listing(listing_string))
            except Exception as e:
                raise type(e)(f"In file '{self.__source_file_path}': {e}") from e
        return listings
   
    def __write_listing_files(self, listings):
        if listings:
            self.__create_directory_if_absent()
        for listing in listings:
            self.__context.listing_name_logger.log_name_appearance(listing.name, self.__source_file_path)
            self.__write_listing_file(listing)

    def __create_directory_if_absent(self):
        try:
            os.mkdir(self.__listing_directory_path)
            self.__context.action_logger.log_created_directory(self.__listing_directory_path)
        except FileExistsError:
            pass

    def __write_listing_file(self, listing):
        write_path = os.path.join(self.__listing_directory_path, listing.name + ListingConstants.LISTING_FILE_EXTENSION)
        with open(write_path, "wt", encoding="utf-8") as f:
            f.write(listing.content)
            self.__context.action_logger.log_written_file(write_path)

    def set_listing_directory(self, directory_path):
        self.__listing_directory_path = directory_path