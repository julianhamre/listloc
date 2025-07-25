class Listing:
    BEGIN_STATEMENT = "BEGIN LISTING"
    END_STATEMENT = "END LISTING"

    def __init__(self, listing_string: str):
        self.__validate_input_string(listing_string)
        self.__listing_lines = listing_string.splitlines()
        self.__begin_statement_line = self.__listing_lines[0].strip()
        self.__begin_statement_keywords = self.__begin_statement_line.split()
        self.__content = self.__extract_content()
        self.__validate_listing()

    def __validate_input_string(self, listing_string):
        if not isinstance(listing_string, str):
            raise TypeError("The listing string must be a string")
        if listing_string == "":
            raise ListingError("The listing string cannot be empty")
        
    def __extract_content(self):
        statement_lines_removed = self.__listing_lines[1:-1]
        content_lines = self.__surrounding_empty_lines_removed(statement_lines_removed)
        return "\n".join(content_lines)
    
    def __surrounding_empty_lines_removed(self, lines):
        lines_copy = lines[:]
        # Remove leading empty lines
        while lines_copy and lines_copy[0].strip() == "":
            lines_copy = lines_copy[1:]
        # Remove trailing empty lines
        while lines_copy and lines_copy[-1].strip() == "":
            lines_copy = lines_copy[:-1]
        return lines_copy
    
    def __validate_listing(self):
        self.__validate_statement_lines()
        self.__validate_content()

    def __validate_statement_lines(self):
        if not len(self.__begin_statement_keywords) == 3:
            self.__raise_begin_statement_format_error()
        if not self.__begin_statement_line.startswith(self.BEGIN_STATEMENT):
            self.__raise_begin_statement_format_error()
        end_line = self.__listing_lines[-1].strip()
        if not end_line.endswith(self.END_STATEMENT):
            raise ListingError(f"The end statement line '{end_line}' should end with '{self.END_STATEMENT}'")

    def __raise_begin_statement_format_error(self):
        raise ListingError(f"The begin statement '{self.__begin_statement_line}' should be in the format '{self.BEGIN_STATEMENT} <name>' (e.g., 'BEGIN LISTING my_snippet')")

    def __validate_content(self):
        if self.__content == "":
            raise ListingError(f"The listing content cannot be empty")

    @property
    def name(self):
        return self.__begin_statement_keywords[2]

    @property
    def content(self):
        return self.__content
    

class ListingError(Exception):

    def __init__(self, message):
        super().__init__(message)