from jinja2 import Template

with open("data/Profile.md") as f:
    chekresh_data = f.read()

prompt_template = Template("""
you are ai assistant of chekresh chatbot you will be given a user message and you will need to respond to the user message.

your name is kushi 
you are a helpful assistant that can answer questions abount chekresh.

user_message: {{ user_message }}

chekresh_data: {{ chekresh_data }}
""")


def render_prompt(user_message: str) -> str:
    return prompt_template.render(
        user_message=user_message, chekresh_data=chekresh_data
    )
