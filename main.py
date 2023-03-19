import gradio as gr
from util import get_existing_books, analyze_file, DATA_PATH

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
