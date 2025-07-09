import re
import os
from snippet import Snippet
import shutil

class SnippetExtractor:
    DIRECTORY_NAME = "code_snippets"

    def __init__(self, source_file_path):
        self.__source_file_path = source_file_path
        self.__parent_directory_path = os.path.dirname(self.__source_file_path)
        self.__snippet_directory_path =  f"{self.__parent_directory_path}/{self.DIRECTORY_NAME}"

    def extract_snippets(self):
        """
        Extracts every valid code snippet from the given source file and saves their contents 
        in their own designated files. The snippet files will be stored in their own directory
        located in the directory of the code file that is extracted from. A valid snippet is 
        the content in between the statements 'BEGIN SNIPPET <name>' and 'END SNIPPET'. 
        The <name> argument decides the snippet file names.
        """
        with open(self.__source_file_path, "rt", encoding="utf-8") as f:
            code = f.read()
            pattern = f"{Snippet.BEGIN_STATEMENT}.*?{Snippet.END_STATEMENT}"
            snippet_strings = re.findall(pattern, code, flags=re.DOTALL)
            snippets = self.__construct_snippets(snippet_strings)
            self.__write_snippet_files(snippets)
    
    def __construct_snippets(self, snippet_strings):
        snippets = []
        for snippet_string in snippet_strings:
            snippets.append(Snippet(snippet_string))
        return snippets
   
    def __write_snippet_files(self, snippets):
        self.__create_directory_if_absent()
        for snippet in snippets:
            self.__write_snippet_file(snippet)

    def __create_directory_if_absent(self):
        try:
            os.mkdir(self.__snippet_directory_path)
        except FileExistsError:
            pass

    def __write_snippet_file(self, snippet):
        write_path = f"{self.__snippet_directory_path}/{snippet.name}.txt"
        with open(write_path, "wt", encoding="utf-8") as f:
            f.write(snippet.content)

    def delete_snippet_directory_if_present(self):
        if os.path.isdir(self.__snippet_directory_path):
            shutil.rmtree(self.__snippet_directory_path)