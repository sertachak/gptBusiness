import os

from flask import Flask
import openai
from dotenv import load_dotenv

import utils.webcrawl

load_dotenv()

app = Flask(__name__)

openai.api_key = os.environ.get("OPEN_AI_APIKEY")

promt = "Can you give a random small sentence just for trying purpose"

@app.route('/')
async def businesstest():  # put application's code here
    print("Inside")
    await utils.webcrawl.crawl("http://hakbilenmedikal.com/")
    # response = openai.chat.completions.create(
    #     messages=[
    #         {
    #             "role": "user",
    #             "content": "Can you give a random small sentence just for trying purpose"
    #         }
    #     ],
    #     model="text-davinci-003"
    # )
    # responseText = response['choices'][0]['text']


if __name__ == '__main__':
    app.run()
