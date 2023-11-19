from flask import Flask
import openai
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)



promt = "Can you give a random small sentence just for trying purpose"

@app.route('/')
def businesstest():  # put application's code here
    print("Inside")
    response = openai.chat.completions.create(
        messages=[
            {
            "role": "user",
            "content": "Can you give a random small sentence just for trying purpose"
            }
        ],
        model="text-davinci-003"
    )
    responseText = response['choices'][0]['text']
    print(responseText)
    return responseText


if __name__ == '__main__':
    app.run()
