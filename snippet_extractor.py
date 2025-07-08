import re
import os
from snippet import Snippet

class SnippetExtractor:
    DIRECTORY_NAME = "code_snippets"   

    def extract_from(self, path: str):
        """
        Extracts every valid code snippet from the given file and saves their contents 
        in their own designated files. The snippet files will be stored in their own directory
        located in the directory of the code file that is extracted from. A valid snippet is 
        the content in between the statements 'BEGIN SNIPPET <name>' and 'END SNIPPET'. 
        The <name> argument decides the snippet file names.

        Args:
           path (str): The path to the file to be extracted from
        """
        with open(path, "rt", encoding="utf-8") as f:
            code = f.read()
            pattern = f"{Snippet.BEGIN_STATEMENT}.*?{Snippet.END_STATEMENT}"
            snippet_strings = re.findall(pattern, code, flags=re.DOTALL)
            snippets = self.__construct_snippets(snippet_strings)
            self.__write_snippet_files(path, snippets)
    
    def __construct_snippets(self, snippet_strings):
        snippets = []
        for snippet_string in snippet_strings:
            snippets.append(Snippet(snippet_string))
        return snippets
   
    def __write_snippet_files(self, path, snippets):
        directory_path = self.__path_to_snippet_directory(path)
        self.__create_directory_if_absent(directory_path)
        for snippet in snippets:
            self.__write_snippet_file(directory_path, snippet)

    def __path_to_snippet_directory(self, file_path):
        code_file_directory_path = os.path.dirname(file_path)
        snippet_directory_path = f"{code_file_directory_path}/{self.DIRECTORY_NAME}"
        return snippet_directory_path

    def __create_directory_if_absent(self, directory_path):
        try:
            os.mkdir(directory_path)
        except FileExistsError:
            pass

    def __write_snippet_file(self, directory_path, snippet):
        write_path = f"{directory_path}/{snippet.name}.txt"
        with open(write_path, "wt", encoding="utf-8") as f:
            f.write(snippet.content)