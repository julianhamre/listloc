from rich import print
from rich.rule import Rule
from listloc.extractor.listing_constants import ListingConstants


class ActionLogger:

    def __init__(self, base_directory_path, verbose=False):
        self.__extracted_files = 0
        self.__created = PathLogger()
        self.__deleted = PathLogger()
        self.__BASE_DIRECTORY_PATH = base_directory_path
        self.__verbose = verbose

    def log_extracted(self, path, number_of_listings):
        if number_of_listings:
            self.__extracted_files += 1
            self.__print_if_verbose(f"Extracted {number_of_listings} listing{self.__plural_suffix(number_of_listings)} from '{path}'")

    def log_written_file(self, path):
        self.__log("Wrote", path, self.__created)

    def log_created_directory(self, path):
        self.__log("Created", path, self.__created)

    def log_deleted_file(self, path):
        self.__log("Deleted", path, self.__deleted)

    def log_removed_directory(self, path):
        self.__log("Removed", path, self.__deleted)

    def __log(self, action_keyword, path, path_logger):
        path_logger.log_path(path)
        self.__print_if_verbose(f"{action_keyword} '{path}'")

    def __print_if_verbose(self, string):
        if self.__verbose:
            print(string)

    def summarize_or_note_no_extractions(self):
        self.__summarize(f"No listings to extract from '{self.__BASE_DIRECTORY_PATH}'")
    
    def summarize_or_note_no_clearings(self):
        self.__summarize(f"Nothing to clear in '{self.__BASE_DIRECTORY_PATH}'")

    def __summarize(self, no_actions_message):
        if self.__no_actions_logged():
            print(no_actions_message)
            return
        self.__print_if_verbose(Rule(characters="--", align="left", style="dim"))
        number_of_deleted_files = self.__deleted.number_of_listing_files()
        self.__print_concluding_message(number_of_deleted_files, f"Deleted a total of {number_of_deleted_files} extracted listing{self.__plural_suffix(number_of_deleted_files)}")
        number_of_written_files = self.__created.number_of_listing_files()
        self.__print_concluding_message(number_of_written_files, f"Extracted a total of {number_of_written_files} listing{self.__plural_suffix(number_of_written_files)} from {self.__extracted_files} source file{self.__plural_suffix(self.__extracted_files)}")

    def __no_actions_logged(self):
        return self.__created.number_of_paths() == 0 and self.__deleted.number_of_paths() == 0
            
    def __print_concluding_message(self, number_of_files, message):
        if number_of_files:
            print(message)

    def __plural_suffix(self, count):
        return "s" if count > 1 else ""


class PathLogger:

    def __init__(self):
        self.__paths = []

    def log_path(self, path: str):
        self.__paths.append(path)

    def number_of_paths(self):
        return len(self.__paths)
    
    def number_of_listing_files(self):
        files = 0
        for path in self.__paths:
            if path.endswith(ListingConstants.LISTING_FILE_EXTENSION):
                files += 1
        return files