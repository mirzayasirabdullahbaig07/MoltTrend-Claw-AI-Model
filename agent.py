import requests
import json
import os
from datetime import datetime
import google.generativeai as genai

from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5")


MEMORY_FILE = "memory.json"


# ------------------------
# FETCH TRENDING COINS
# ------------------------
def fetch_trends():
    url = "https://api.coingecko.com/api/v3/search/trending"
    response = requests.get(url)
    data = response.json()
    coins = [coin["item"]["name"] for coin in data["coins"]]
    return coins


# ------------------------
# MEMORY FUNCTIONS
# ------------------------
def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return []

    try:
        with open(MEMORY_FILE, "r") as f:
            content = f.read().strip()
            if not content:
                return []
            return json.loads(content)
    except json.JSONDecodeError:
        return []

# ------------------------
# ANALYZE WITH LLM
# ------------------------
def analyze_trends(trends, history):
    prompt = f"""
    Today's trending cryptocurrencies:
    {trends}

    Previous reports:
    {history[-3:]}

    Provide:
    1. Main narrative themes
    2. Market sentiment
    3. Short-term outlook
    4. Any repeating patterns
    """

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        # Log error to console for debugging
        print(f"AI analysis skipped due to model error: {e}")
        # Return a friendly placeholder instead of the raw exception
        return "AI analysis unavailable at this time."




# ------------------------
# MAIN AGENT RUN
# ------------------------
def run_agent():
    trends = fetch_trends()
    history = load_memory()
    report = analyze_trends(trends, history)
    save_memory(report, trends)
    return report, trends


def save_memory(report, trends):
    memory = load_memory()

    memory.append({
        "date": str(datetime.now()),
        "trends": trends,
        "report": report
    })

    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)
