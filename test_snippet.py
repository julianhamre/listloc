import unittest
from snippet import Snippet, SnippetError

class TestSnippet(unittest.TestCase):

    def test_invalid_inputs(self):
        invalid_inputs = [
            "",
            "BEGIN SNIPPET",
            "BEGIN SNIPPET \n END SNIPPET",
            "BEGIN SNIPPET \n\n # END SNIPPET",
            "BEGIN SNIPPET name code # END SNIPPET",
            "BEGIN SNIPPET name name2\n code\n # END SNIPPET",
            "something BEGIN SNIPPET name\n code\n # END SNIPPET",
            "BEGIN SNIPPET name\n code\n # END SNIPPET name"]
        for snippet_string in invalid_inputs:
            self.assertRaises(SnippetError, Snippet, snippet_string)
        self.assertRaises(TypeError, Snippet, 1)

    def test_name(self):
        expected_name = "Snippet_name"
        snippet_string = "BEGIN SNIPPET " + expected_name +"\n some\n code\n END SNIPPET"
        my_snippet = Snippet(snippet_string)
        actual_name = my_snippet.name
        self.assertEqual(expected_name, actual_name)

    def test_content(self):
        snippet_strings = ["BEGIN SNIPPET name\n\nprint('hello')\n\n\n  # END SNIPPET",
                           "BEGIN SNIPPET name2 \n    print('Hello world')\n\n % END SNIPPET",
                           "BEGIN SNIPPET NaMe_03\n\n\n    print('one')\n\n\n\nprint('two')\n    a = 1 + 2\n# END SNIPPET"]
        expected_content_strings = ["print('hello')", 
                                    "    print('Hello world')",
                                    "    print('one')\n\n\n\nprint('two')\n    a = 1 + 2"]
        for i in range(len(snippet_strings)):
            self.__assert_correct_content(snippet_strings[i], expected_content_strings[i])

    def __assert_correct_content(self, snippet_string, expected_content):
        actual_content = Snippet(snippet_string).content
        self.assertEqual(expected_content, actual_content)

if __name__ == "__main__":
    unittest.main()