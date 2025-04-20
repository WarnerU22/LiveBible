from flask import Flask, render_template, request
from dotenv import load_dotenv
from openai import OpenAI
import os

# Load .env file (for local development — Render uses its own environment tab)
load_dotenv()

# OpenAI client will auto-read from the OPENAI_API_KEY in environment
client = OpenAI()

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    response_text = ""
    if request.method == "POST":
        user_input = request.form.get("prompt", "")

        messages = [
            {
                "role": "system",
                "content": (
                    "You are a helpful Christian assistant. "
                    "When someone shares a struggle, respond with a relevant Bible verse, "
                    "a short prayer, and one sentence of encouragement."
                )
            },
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
