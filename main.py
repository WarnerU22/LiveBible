from flask import Flask, render_template, request
from dotenv import load_dotenv
import openai
import os

# Load env file
load_dotenv()

# Set API key for old OpenAI client
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    response_text = ""
    if request.method == "POST":
        user_input = request.form["prompt"]

        messages = [
            {"role": "system", "content": "You are a helpful Christian assistant. When someone shares a struggle, respond with a relevant Bible verse, a short prayer, and a sentence of encouragement."},
            {"role": "user", "content": user_input}
        ]

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages
            )
            response_text = response["choices"][0]["message"]["content"].strip()
        except Exception as e:
            response_text = f"❌ Error: {e}"

    return render_template("index.html", response=response_text)


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/mission")
def mission():
    return render_template("mission.html")


@app.route("/help")
def help_page():
    return render_template("help.html")


@app.route("/verse")
def verse():
    verses = [
        "For God so loved the world, that he gave his only Son (John 3:16)",
        "The LORD is my shepherd; I shall not want (Psalm 23:1)",
        "I can do all things through Christ who strengthens me (Philippians 4:13)",
    ]
    import random
    return render_template("verse.html", verse=random.choice(verses))

if __name__ == "__main__":
    app.run(debug=True)
