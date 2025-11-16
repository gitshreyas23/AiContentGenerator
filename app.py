import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import google.generativeai as genai

# Load API key
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("Please set GOOGLE_API_KEY in .env file")

# Configure Gemini
genai.configure(api_key=GOOGLE_API_KEY)

app = Flask(__name__, static_folder="static", template_folder="templates")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    topic = data.get("topic", "")
    content_type = data.get("content_type", "paragraph")
    length = data.get("length", "short")

    if not topic:
        return jsonify({"error": "Topic is required"}), 400

    # Length mapping
    length_map = {
        "short": "short (2–4 sentences)",
        "medium": "medium (5–8 sentences)",
        "long": "long (3–4 paragraphs)"
    }
    length_desc = length_map.get(length, "short")

    # Build prompt
    if content_type == "blog":
        prompt = f"Write a {length_desc} beginner-friendly blog post on '{topic}' with title and bullet points."
    elif content_type == "social":
        prompt = f"Write 3 short social media captions for '{topic}'."
    else:
        prompt = f"Write a {length_desc} paragraph about '{topic}'."

    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
 

        response = model.generate_content(prompt)

        return jsonify({"result": response.text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
