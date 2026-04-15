from flask import Flask, render_template, request, jsonify
from scraper import analyze_site

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    url = data.get('url')

    if not url:
        return jsonify({"error": "اكتب رابط"}), 400

    result = analyze_site(url)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
