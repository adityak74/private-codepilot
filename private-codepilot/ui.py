import gradio as gr
from pathlib import Path
from langchain_chroma import Chroma
from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)

REPO_DIR = Path(__file__).parent.resolve()
PERSIST_DIR = "/Users/adityakarnam/PycharmProjects/ff-routing-fastapi/chroma_db"
LLM = "codellama:7b-instruct"
BASE_URL = "http://localhost:11434"

ollama = Ollama(base_url=BASE_URL, model=LLM)
embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = Chroma(
    embedding_function=embedding_function, persist_directory=PERSIST_DIR
)
qachain = RetrievalQA.from_chain_type(ollama, retriever=vectorstore.as_retriever())

GIT_BRANCH = "main"


def set_git_branch(value):
    global GIT_BRANCH
    print(f"Setting git branch {GIT_BRANCH} to {value}")
    GIT_BRANCH = value

def yes_man(message, history):
    print(history, GIT_BRANCH)
    answer = qachain.invoke({"query": message})
    return answer["result"]


# Define the ChatInterface
chat_interface = gr.ChatInterface(
    yes_man,
    chatbot=gr.Chatbot(height=400),
    textbox=gr.Textbox(
        placeholder="How can I help?", container=False, scale=7
    ),
    description=f"Active Repo: {REPO_DIR}",
    theme="base",
    cache_examples=True,
    retry_btn=None,
    undo_btn="Delete Previous",
    clear_btn="Clear",
)

css = """
#app_title {
  margin: auto;
  width: 50%;
  padding: 10px;
  text-align: center;
}
"""

# Use Blocks to structure the layout
with gr.Blocks(css=css) as demo:

    with gr.Row(variant="default"):
        with gr.Column(scale=1, min_width=0):
            pass  # Empty column to center the content
        with gr.Column(scale=1, min_width=0, elem_id="app_title"):
            gr.Markdown("# Zefr-Copilot")
        with gr.Column(scale=1, min_width=0):
            pass  # Empty column to center the content

    with gr.Row(variant="default"):
        git_branch_textbox = gr.Textbox(
            info="The branch you are developing",
            label="git_branch",
            placeholder=GIT_BRANCH,
            elem_id="git_branch",
            key="git_branch",
        )
        git_branch_textbox.change(
            fn=set_git_branch,
            inputs=git_branch_textbox
        )

    with gr.Column():
        # Add the chat interface within the column
        chat_interface.render()

    # Additional inputs or components can be added here if needed
    # For example, a button to clear the chat history or reset inputs
    with gr.Row():
        clear_button = gr.Button("Clear Chat History")


    # Define the action for the clear button
    def clear_chat_history():
        return gr.update(value=[])


    clear_button.click(clear_chat_history, outputs=chat_interface.chatbot)

if __name__ == "__main__":
    demo.launch()
