import openai
from constants import OPENAI_API_KEY, HEADER_LENGTH

# AI helper methods
openai.api_key = OPENAI_API_KEY


def get_ai_response(prompt, model="gpt-3.5-turbo", max_tokens=100):
    if OPENAI_API_KEY == "":
        return "AI response"

    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a chatbot in a chat."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=max_tokens,
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"An error occurred: {str(e)}"


def get_ai_generated_string():
    return get_ai_response("Say something completely new and unrelated")


def get_ai_generated_response(previous_chat_lines):
    prompt = (f"This is the previous chat lines: {previous_chat_lines} please send a responce")
    return get_ai_response(prompt)


# message helper methods
def extract_message_length(header):
    return int(header.decode("utf-8").strip())


def extract_message(message):
    return message["data"].decode("utf-8")


def extract_message_header(message):
    return f"{len(message):<{HEADER_LENGTH}}".encode("utf-8")


def message_to_bytes(message):
    return message["header"] + message["data"]
