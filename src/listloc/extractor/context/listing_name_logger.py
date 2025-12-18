from listloc.extractor.listing import ListingError

class ListingNameLogger:

    def __init__(self):
        self.__appearances = {}
        self.__duplicate_name = False

    def log_name_appearance(self, name, file_path):
        if not name in self.__appearances:
            self.__appearances[name] = {file_path: 1}
            return
        self.__duplicate_name = True
        if not file_path in self.__appearances[name]:
            self.__appearances[name][file_path] = 1
        else:
            self.__appearances[name][file_path] += 1

    def ensure_all_names_are_unique(self):
        if not self.__duplicate_name:
            return
        for name in self.__appearances:
            self.__ensure_is_unique(name)
    
    def __ensure_is_unique(self, name):
        if len(self.__appearances[name]) > 1:
            self.__raise_not_unique_error(name)
        files_appeared_in = self.__appearances[name]
        for file in files_appeared_in:
            if files_appeared_in[file] > 1:
                self.__raise_not_unique_error(name) 
    
    def __raise_not_unique_error(self, name):
        message = f"The listing name '{name}' must only be used to name one listing. It is currently used:"
        for file in self.__appearances[name]:
            appearances_in_file = self.__appearances[name][file]
            message += f"\n- {appearances_in_file} {self.__time_conjugated(appearances_in_file)} in '{file}'"
        raise ListingError(message)

    def __time_conjugated(self, appearances):
        if appearances == 1:
            return "time"
        return "times"
        