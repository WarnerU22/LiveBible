from flask import Flask, render_template, request
from dotenv import load_dotenv
from openai import OpenAI
import os

# Load .env and API key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    response_text = ""
    if request.method == "POST":
        user_input = request.form["prompt"]

        messages = [
            {"role": "system", "content": "You are a helpful Christian assistant. When someone shares a struggle, you respond with a relevant Bible verse, a short prayer, and a sentence of encouragement."},
            {"role": "user", "content": user_input}
        ]

        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages
            )
            response_text = response.choices[0].message.content.strip()
        except Exception as e:
            response_text = f"❌ Error: {e}"

    return render_template("index.html", response=response_text)

if __name__ == "__main__":
    app.run(debug=True)

