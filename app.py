from flask import Flask, render_template, request, jsonify
from scraper import WebInsightPro
import os

app = Flask(__name__)


# Home page
@app.route("/")
def home():
    return render_template("index.html")


# Analyze API
@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No data received"}), 400

        url = data.get("url")

        if not url:
            return jsonify({"error": "No URL provided"}), 400

        # Run scraper
        tool = WebInsightPro(url)
        error = tool.fetch_data()

        if error:
            return jsonify({"error": str(error)}), 500

        report = tool.full_report()

        # Ensure keys exist (avoid frontend crash)
        response = {
            "seo_score": report.get("seo_score", 0),
            "title": report.get("title", "N/A"),
            "description": report.get("description", "N/A"),
            "headings": report.get("headings", {"h1": 0, "h2": 0, "h3": 0}),
            "links": report.get("links", {"internal": 0, "external": 0}),
            "suggestions": report.get("suggestions", [])
        }

        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route("/health")
def health():
    return "OK", 200


# Run server
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
