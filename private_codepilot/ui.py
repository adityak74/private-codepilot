import gradio as gr
from private_codepilot import PrivateCodepilot

private_codepilot = PrivateCodepilot()
private_codepilot.setup()
active_repo = private_codepilot.get_active_repo()


def set_git_branch(value):
    global GIT_BRANCH
    if value != "":
        print(f"Setting git branch {GIT_BRANCH} to {value}")
        GIT_BRANCH = value


def yes_man(message, history, git_branch):
    print("message and history------>>>", message, history, git_branch)
    answer = private_codepilot.get_qa_chain().invoke({"query": message})
    return answer["result"]


demo = gr.ChatInterface(
    yes_man,
    chatbot=gr.Chatbot(height=400),
    textbox=gr.Textbox(
        placeholder=f"Current Repo: {active_repo}", container=False, scale=7
    ),
    title="Private-Codepilot",
    description="Ask any questions",
    theme="soft",
    examples=None,
    cache_examples=True,
    retry_btn=None,
    undo_btn="Delete Previous",
    clear_btn="Clear",
    additional_inputs=[
        gr.Textbox(
            info="The branch you are developing",
            label="git_branch",
            placeholder="main",
            elem_id="git_branch",
            key="git_branch",
        )
    ],
)


if __name__ == "__main__":
    demo.launch()
