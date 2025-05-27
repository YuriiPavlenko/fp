import sys
from openai import OpenAI

client = OpenAI()
SYSTEM_PROMPT = """You are a professional Arch Linux assistant. The user will describe the software or library they want to install (e.g., "a tool to convert PDFs to images" or "a C++ library for parsing JSON"). Your job is to:

    Understand what the user wants to install.

    Search the official Arch repos and AUR (Arch User Repository) for the exact package name(s).

    Return numbered list of suitable commands to use in python code and then help the user to identify which one he needs.

    Explain briefly what the package does and why it matches the user’s request.

Only give packages that actually exist and are up to date. Never make up package names.

In the end print numbered list of commands to run in the following format:
{{{
    1. command1
    2. command2
    ...
}}}"""


history = []

def parse_args():
    text = sys.argv[1]
    print(text)
    return text


def ask_gpt():
    return client.responses.create(
        model="gpt-4.1",
        instructions=SYSTEM_PROMPT,
        input=history,
        tools=[{"type": "web_search_preview"}],
        # response_format={"type": "json_object"},
    )

# def user_input_and_chat_response(user_input):
    # sys.stdin.readline()


if __name__ == "__main__":
    text = parse_args()
    history.append({'role': "user", 'content': text})
    gpt_response = ask_gpt()
    history.append({'role': "assistant", 'content': gpt_response.output_text})
    print(history)
    print(gpt_response.output_text)

    for i in range(10):
        user_input = input()
        history.append({'role': "user", 'content': user_input})
        gpt_response = ask_gpt()
        history.append({'role': "assistant", 'content': gpt_response.output_text})
        print(history)
        print(gpt_response.output_text)

