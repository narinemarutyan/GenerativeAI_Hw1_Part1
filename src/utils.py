import requests
import openai

from settings import ENV_VARS

openai.api_key = ENV_VARS.KEY

messages = [{"role": "system",
             "content": "Don't make assumptions about what values to plug into functions. Ask for clarification if a user request is ambiguous."}]


def chat_completion_request(messages, tools=None, tool_choice=None, model=ENV_VARS.GPT_MODEL):
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + openai.api_key,
    }
    json_data = {"model": model, "messages": messages}
    if tools is not None:
        json_data.update({"tools": tools})
    if tool_choice is not None:
        json_data.update({"tool_choice": tool_choice})
    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=json_data,
        )
        return response
    except Exception as e:
        print("Unable to generate ChatCompletion response")
        print(f"Exception: {e}")
        return e
