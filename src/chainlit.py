import chainlit as cl
import openai
import requests

from settings import ENV_VARS
from tools import tools
from utils import chat_completion_request, messages


@cl.on_message
async def main(message: cl.Message):
    messages.append({"role": "user", "content": message.content})
    response = chat_completion_request(messages, tools=tools).json()["choices"][0]["message"]
    messages.append(response)

    if not response["content"]:
        loc = response['tool_calls'][0]['function']['arguments'].split('"')[3]

        url = "http://api.openweathermap.org/data/2.5/weather"
        openai.api_key = ENV_VARS.KEY
        params = {"q": loc, "APPID": "3128f76a7551a274746e884fd29a0e8f"}

        weather_response = requests.get(url, params=params)

        client = openai.OpenAI(api_key=openai.api_key)
        response = client.chat.completions.create(
            model=ENV_VARS.GPT_MODEL,
            response_format={"type": "text"},
            messages=[{"role": "system", "content": "You are weather assistant"},
                      {"role": "user",
                       "content": f"{weather_response.text} based on this information what the temerature in celcius in the given location. Provide short answer."}])
        processed_response = response.choices[0].message.content

        response = client.chat.completions.create(
            model=ENV_VARS.GPT_MODEL,
            response_format={"type": "text"},
            messages=[
                {"role": "system", "content": "You are an 'English to Armenian' translator."},
                {"role": "user", "content": f"{processed_response} translate this text to Armenian."}
            ]
        )
        armenian_response = response.choices[0].message.content

        response = client.audio.speech.create(model="tts-1-hd", voice="alloy", input=armenian_response)
        response.stream_to_file("weather_in_armenian.mp3")

        response = client.images.generate(model="dall-e-2", prompt=processed_response, size="1024x1024", quality="hd",
                                          n=1)
        image_url = response.data[0].url

        response = client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "What’s in this image?"},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": image_url,
                                "detail": "high"
                            },
                        },
                    ],
                }
            ],
            max_tokens=300,
        )

        extracted_text = response.choices[0].message.content

        content = [processed_response, armenian_response, image_url, extracted_text]
    else:
        content = response["content"]
    await cl.Message(
        content=content,
    ).send()
