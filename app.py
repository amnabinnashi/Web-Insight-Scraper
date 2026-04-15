from flask import Flask, render_template, request, jsonify
from scraper import WebInsightPro
import os

app = Flask(__name__)

# Home route
@app.route("/")
def home():
    return render_template("index.html")


# Analyze endpoint
@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    url = data.get("url")

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    tool = WebInsightPro(url)
    error = tool.fetch_data()

    if error:
        return jsonify({"error": error}), 500

    report = tool.full_report()

    return jsonify({
        "report": report
    })


# Run server (Render compatible)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
