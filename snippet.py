class Snippet:
    BEGIN_STATEMENT = "BEGIN SNIPPET"
    END_STATEMENT = "END SNIPPET"

    def __init__(self, snippet_string: str):
        self.__validate_input_string(snippet_string)
        self.__snippet_lines = snippet_string.splitlines()
        self.__begin_statement_line = self.__snippet_lines[0].strip()
        self.__begin_statement_keywords = self.__begin_statement_line.split(" ")
        self.__content = "\n".join(self.__snippet_lines[1:-1])
        self.__validate_snippet()

    def __validate_input_string(self, snippet_string):
        if not isinstance(snippet_string, str):
            raise TypeError("The snippet_string must be a string")
        if snippet_string == "":
            raise SnippetError("The snippet_string cannot be empty")
    
    def __validate_snippet(self):
        self.__validate_statement_lines()
        self.__validate_content()

    def __validate_statement_lines(self):
        if not len(self.__begin_statement_keywords) == 3:
            self.__raise_begin_statement_format_error()
        if not self.__begin_statement_line.startswith(self.BEGIN_STATEMENT):
            self.__raise_begin_statement_format_error()
        end_line = self.__snippet_lines[-1].strip()
        if not end_line == self.END_STATEMENT:
            raise SnippetError(f"The end statement '{end_line}' should be '{self.END_STATEMENT}'")

    def __raise_begin_statement_format_error(self):
        raise SnippetError(f"The begin statement '{self.__begin_statement_line}' should be on the format '{self.BEGIN_STATEMENT} <name>'")

    def __validate_content(self):
        if self.__content == "":
            raise SnippetError(f"The snippet content cannot be empty")

    @property
    def name(self):
        return self.__begin_statement_keywords[2]

    @property
    def content(self):
        return self.__content
    

class SnippetError(Exception):

    def __init__(self, message):
        super().__init__(message)