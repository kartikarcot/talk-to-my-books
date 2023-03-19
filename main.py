# create an index with the text and save it to disk in data/indexes
from llama_index import GPTSimpleVectorIndex
import os
from IPython.display import Markdown, display
os.environ["OPENAI_API_KEY"] = "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"
import gradio as gr
import os
import glob
import unittest
DATA_PATH = "./data/epubs/"

def get_existing_books(path):
    # return a list of the existing books
    # trim any trailing / from the path
    if path[-1] == "/":
        path = path[:-1]
    bookdirpaths = glob.glob(path + "/*")
    # find a file which matches a format specified in the formats list and has the same name as the directory
    formats = [".epub", ".mobi", ".pdf", ".txt"]
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
        filepath), os.path.basename(os.path.dirname(filepath)) + ".json")
    if os.path.exists(index_path):
        return index_path
    else:
        return None


def create_index(filename) -> str:
    # Create an index for the file and save it to the indexpath
    return None


def get_or_create_index(filepath):
    ret = get_existing_index(filepath)
    if ret is None:
        return create_index(filepath)
    return ret


def answer_query(filepath, query):
    # Get the index for the file
    index = GPTSimpleVectorIndex.load_from_disk(get_or_create_index(filepath))
    # Use the index to answer the query
    return f"<b>{index.query(query)}</b>"


def analyze_file(file, dropdown, query):
    # now print the file to analyze and the query in the output box
    ret, err_str = validate_inputs(file, dropdown, query)
    if ret:
        return answer_query(get_filepath_to_analyze(file, dropdown), query)
    else:
        return err_str

def create_app():
    # inputs is a list of a file input option and a dropdown option showing the already
    # existing files in the directory. The dropdown box is named "Choose From Existing Files"
    # and the file input box is named "Upload New File". inputs also has a box for input query.
    description = "Talk to My Books is a tool that allows you to ask questions about a book and get answers." \
                    " Built by <a href='https://twitter.com/kartikarcot'> Kartik Arcot </a> and <a href='https://twitter.com/HSlifelearner'> Harsh Sharma </a>." \
                    " Powered by openai and llama-index!"
    inputs = [gr.File(),
            gr.Dropdown(list(get_existing_books(DATA_PATH).keys()),
                        label="Choose From Existing Files"),
            gr.Textbox(label="Query")]
    outputs = gr.HTML()
    app = gr.Interface(analyze_file, inputs, outputs, title="Talk To My Books", description = description)
    return app

if __name__ == "__main__":
    app = create_app()
    app.launch()
