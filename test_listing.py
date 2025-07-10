import unittest
from listing import Listing, ListingError

class TestListing(unittest.TestCase):

    def test_invalid_inputs(self):
        invalid_inputs = [
            "",
            "BEGIN LISTING",
            "BEGIN LISTING \n END LISTING",
            "BEGIN LISTING \n\n # END LISTING",
            "BEGIN LISTING name code # END LISTING",
            "BEGIN LISTING name name2\n code\n # END LISTING",
            "something BEGIN LISTING name\n code\n # END LISTING",
            "BEGIN LISTING name\n code\n # END LISTING name"]
        for listing_string in invalid_inputs:
            self.assertRaises(ListingError, Listing, listing_string)
        self.assertRaises(TypeError, Listing, 1)

    def test_name(self):
        expected_name = "Listing_name"
        listing_string = "BEGIN LISTING " + expected_name +"\n some\n code\n END LISTING"
        my_listing = Listing(listing_string)
        actual_name = my_listing.name
        self.assertEqual(expected_name, actual_name)

    def test_content(self):
        listing_strings = ["BEGIN LISTING name\n\nprint('hello')\n\n\n  # END LISTING",
                           "BEGIN LISTING name2 \n    print('Hello world')\n\n % END LISTING",
                           "BEGIN LISTING NaMe_03\n\n\n    print('one')\n\n\n\nprint('two')\n    a = 1 + 2\n# END LISTING"]
        expected_content_strings = ["print('hello')", 
                                    "    print('Hello world')",
                                    "    print('one')\n\n\n\nprint('two')\n    a = 1 + 2"]
        for i in range(len(listing_strings)):
            self.__assert_correct_content(listing_strings[i], expected_content_strings[i])

    def __assert_correct_content(self, listing_string, expected_content):
        actual_content = Listing(listing_string).content
        self.assertEqual(expected_content, actual_content)

if __name__ == "__main__":
    unittest.main()