from flask import Flask, render_template, request
from dotenv import load_dotenv
import openai
import os

# Load env file and set API key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(
    __name__,
    template_folder="../frontend/templates",
    static_folder="../frontend/static",
)



@app.route("/", methods=["GET", "POST"])
def home():
    response_text = ""
    if request.method == "POST":
        user_input = request.form["prompt"]
        messages = [
            {
                "role": "system",
                "content": "You are a helpful Christian assistant. When someone shares a struggle, respond with a relevant Bible verse, a short prayer, and a sentence of encouragement.",
            },
            {"role": "user", "content": user_input},
        ]
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", messages=messages
            )
            response_text = response["choices"][0]["message"]["content"].strip()
        except Exception as e:
            response_text = f"❌ Error: {e}"
    return render_template("index.html", response=response_text)


@app.route("/about")
def about():
    return render_template("about.html")




@app.route("/faq")
def faq():
    return render_template("faq.html")


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/mission")
def mission():
    return render_template("mission.html")


@app.route("/help")
def help_page():
    return render_template("help.html")


@app.route("/verses", methods=["GET", "POST"])
def verses():
    results = ""
    topic = ""
    if request.method == "POST":
        topic = request.form["topic"]
        messages = [
            {
                "role": "system",
                "content": (
                    "Provide five short Bible verses with references that speak to the given topic. Keep the tone uplifting and return them as bullet points with a blank line between each item for easy reading."
                ),
            },
            {"role": "user", "content": topic},
        ]
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", messages=messages
            )
            results = response["choices"][0]["message"]["content"].strip()
        except Exception as e:
            results = f"❌ Error: {e}"
    return render_template("verses.html", topic=topic, results=results)
