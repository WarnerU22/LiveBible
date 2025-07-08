from flask import Flask, render_template, request
from dotenv import load_dotenv
from datetime import date
import openai
import os

# Load env file and set API key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__, template_folder="../frontend/templates", static_folder="../frontend/static")

# Track daily usage per IP
USAGE_LIMIT = 20
usage_log = {}
premium_users = set()

def _reset_if_new_day(record):
    today = date.today()
    if record.get('date') != today:
        record['date'] = today
        record['count'] = 0

def increment_usage(ip):
    record = usage_log.setdefault(ip, {'date': date.today(), 'count': 0})
    _reset_if_new_day(record)
    record['count'] += 1

def limit_reached(ip):
    if ip in premium_users:
        return False
    record = usage_log.setdefault(ip, {'date': date.today(), 'count': 0})
    _reset_if_new_day(record)
    return record['count'] >= USAGE_LIMIT

@app.route('/', methods=['GET', 'POST'])
def home():
    response_text = ''
    ip = request.remote_addr
    show_modal = False
    if request.method == 'POST':
        if limit_reached(ip):
            show_modal = True
        else:
            increment_usage(ip)
            user_input = request.form['prompt']
            messages = [
                {"role": "system", "content": "You are a helpful Christian assistant. When someone shares a struggle, respond with a relevant Bible verse, a short prayer, and a sentence of encouragement."},
                {"role": "user", "content": user_input}
            ]
            try:
                response = openai.ChatCompletion.create(model='gpt-3.5-turbo', messages=messages)
                response_text = response['choices'][0]['message']['content'].strip()
            except Exception as e:
                response_text = f"❌ Error: {e}"
    return render_template('index.html', response=response_text, limit_reached=show_modal)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/pricing')
def pricing():
    return render_template('pricing.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/upgrade')
def upgrade():
    return render_template('upgrade.html')

@app.route('/upgrade/complete', methods=['POST'])
def upgrade_complete():
    premium_users.add(request.remote_addr)
    return render_template('upgrade_success.html')

@app.route('/mission')
def mission():
    return render_template('mission.html')

@app.route('/help')
def help_page():
    return render_template('help.html')

@app.route('/verses', methods=['GET', 'POST'])
def verses():
    results = ''
    topic = ''
    ip = request.remote_addr
    show_modal = False
    if request.method == 'POST':
        if limit_reached(ip):
            show_modal = True
        else:
            increment_usage(ip)
            topic = request.form['topic']
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
                response = openai.ChatCompletion.create(model='gpt-3.5-turbo', messages=messages)
                results = response['choices'][0]['message']['content'].strip()
            except Exception as e:
                results = f"❌ Error: {e}"
    return render_template('verses.html', topic=topic, results=results, limit_reached=show_modal)
