import unittest
import os
from util import get_existing_books, get_filepath_to_analyze, validate_inputs, get_existing_index, create_index, get_or_create_index, copy_new_book_to_data

# write unit tests for the above functions
TEST_DATA_PATH = "./test_data/epubs/"


class TestFile:
    def __init__(self, name):
        self.name = name


class TestInferenceHelpers(unittest.TestCase):
    def test_get_existing_books(self):
        books = get_existing_books(TEST_DATA_PATH)
        self.assertEqual(len(books), 1)
        self.assertEqual(books["Seeing Like A State"],
                         "./test_data/epubs/Seeing Like A State/Seeing Like A State.epub")

    def test_get_file_to_analyze(self):
        self.assertEqual(get_filepath_to_analyze(
            None, "Seeing Like A State", TEST_DATA_PATH), "./test_data/epubs/Seeing Like A State/Seeing Like A State.epub")

        self.assertEqual(get_filepath_to_analyze(TestFile("./test_data/epubs/Seeing Like A State/Seeing Like A State.epub"),
                         None, TEST_DATA_PATH), "./test_data/epubs/Seeing Like A State/Seeing Like A State.epub")

    def test_validate_inputs(self):
        self.assertEqual(validate_inputs(None, None, "query"), (False,
                         "[ERROR] Either upload a file or choose from existing files."))
        self.assertEqual(validate_inputs(None, "Seeing Like A State", ""),
                         (False, "[ERROR] Query input cannot be empty."))
        self.assertEqual(validate_inputs(
            None, "Seeing Like A State", "query"), (True, ""))
        self.assertEqual(validate_inputs(TestFile("./test_data/epubs/Seeing Like A State/Seeing Like A State.epub"),
                         None, "query"), (True, ""))

    def test_get_existing_index(self):
        self.assertEqual(get_existing_index("./test_data/epubs/Seeing Like A State/Seeing Like A State.epub"),
                         "./test_data/epubs/Seeing Like A State/Seeing Like A State.json")

    def test_create_index(self):
        self.assertEqual(create_index("./test_data/epubs/Seeing Like A State/Seeing Like A State.epub", test=True),
                         "./test_data/epubs/Seeing Like A State/Seeing Like A State.json")

    def test_get_or_create_index(self):
        self.assertEqual(get_or_create_index("./test_data/epubs/Seeing Like A State/Seeing Like A State.epub"),
                         "./test_data/epubs/Seeing Like A State/Seeing Like A State.json")

    def test_copy_new_book_to_data(self):
        if os.path.exists("./test_data/epubs/Seeing Like A State New"):
            os.remove("./test_data/epubs/Seeing Like A State New/Seeing Like A State.epub")
            os.remove("./test_data/epubs/Seeing Like A State New/Seeing Like A State.json")
            os.rmdir("./test_data/epubs/Seeing Like A State New")
        
        self.assertEqual(copy_new_book_to_data("./test_data/epubs/Seeing Like A State/Seeing Like A State.epub",
                         "./test_data/epubs/Seeing Like A State/Seeing Like A State.json", "Seeing Like A State New", TEST_DATA_PATH),
                         "./test_data/epubs/Seeing Like A State New")
        # ensure the new book is copied to the data directory
        self.assertTrue(os.path.exists("./test_data/epubs/Seeing Like A State New/Seeing Like A State.epub"))
        self.assertTrue(os.path.exists("./test_data/epubs/Seeing Like A State New/Seeing Like A State.json"))
        
        # now delete the new book
        os.remove("./test_data/epubs/Seeing Like A State New/Seeing Like A State.epub")
        os.remove("./test_data/epubs/Seeing Like A State New/Seeing Like A State.json")
        os.rmdir("./test_data/epubs/Seeing Like A State New")
        


if __name__ == "__main__":
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
