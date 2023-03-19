# create an index with the text and save it to disk in data/indexes
import unittest
import glob
from llama_index import GPTSimpleVectorIndex, SimpleDirectoryReader
import os
from IPython.display import Markdown, display
from shutil import copy
os.environ["OPENAI_API_KEY"] = "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"
DATA_PATH = "./data/epubs/"


def get_existing_books(path):
    # return a list of the existing books
    # trim any trailing / from the path
    if path[-1] == "/":
        path = path[:-1]
    bookdirpaths = glob.glob(path + "/*")
    # find a file which matches a format specified in the formats list and has the same name as the directory
    formats = [".epub", ".pdf", ".txt"]
    bookpaths = []
    for bookdir in bookdirpaths:
        for format in formats:
            book = os.path.join(bookdir, os.path.basename(bookdir) + format)
            if os.path.exists(book):
                bookpaths.append(book)
                break
    # return a dict with key being only the book name without any path information or format specifier
    return {os.path.basename(bookpath).split(".")[0]: bookpath for bookpath in bookpaths}

# output function that takes in the file, the dropdown option, and the input query
# and returns the output of the query


def get_filepath_to_analyze(file, dropdown: str, data_path: str = DATA_PATH):
    if file is not None:
        return file.name
    elif dropdown is not None:
        return get_existing_books(data_path)[dropdown]


def validate_inputs(file, dropdown, query):
    # Check that either a file is uploaded or a dropdown option is selected
    if (not file) and (not dropdown):
        return False, "[ERROR] Either upload a file or choose from existing files."

    # Check that the query input is not empty
    if not query:
        return False, "[ERROR] Query input cannot be empty."
    return True, ""


def get_existing_index(filepath) -> str:
    # Check if there is a .json file in the same directory with the same name as the filename
    index_path = os.path.join(os.path.dirname(
        filepath), os.path.basename(filepath).split('.')[0] + ".json")
    print("[INFO] Checking for index at: ", index_path)
    if os.path.exists(index_path):
        return index_path
    else:
        return None


def create_index(filepath, test=False) -> str:
    print("[INFO] Creating index for file: ", filepath)
    # Create an index for the file and save it to the indexpath
    docs = SimpleDirectoryReader(None, input_files=[filepath]).load_data()
    indexname = os.path.join(os.path.dirname(
        filepath), os.path.basename(filepath).split('.')[0] + ".json")
    if not test:
        index = GPTSimpleVectorIndex(documents=docs)
        index.save_to_disk(indexname)
    return indexname


def copy_new_book_to_data(filepath, indexpath, bookname, data_path: str = DATA_PATH):
    # Copy the book to the data directory
    new_book_path = os.path.join(data_path, bookname)
    os.mkdir(new_book_path)
    copy(filepath, new_book_path)
    copy(indexpath, new_book_path)
    return new_book_path


def create_and_move_index(filepath, bookname):
    indexpath = create_index(filepath)
    bookpath = copy_new_book_to_data(filepath, indexpath, bookname)
    return os.path.join(bookpath, os.path.basename(indexpath))


def get_or_create_index(filepath):
    print("[INFO] Getting index for file: ", filepath)
    ret = get_existing_index(filepath)
    if ret is None:
        return create_and_move_index(filepath, os.path.basename(filepath).split('.')[0])
    return ret


def answer_query(filepath, query):
    print("[INFO] Answering query: ", query)
    # Get the index for the file
    index = GPTSimpleVectorIndex.load_from_disk(get_or_create_index(filepath))
    # Use the index to answer the query
    return f"<b>{index.query(query,similarity_top_k=1)}</b>"


def analyze_file(file, dropdown, query):
    # now print the file to analyze and the query in the output box
    ret, err_str = validate_inputs(file, dropdown, query)
    if ret:
        return answer_query(get_filepath_to_analyze(file, dropdown), query)
    else:
        return err_str
