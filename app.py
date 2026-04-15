from flask import Flask, render_template, request, jsonify
from scraper import WebInsightPro

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    url = data.get('url')

    tool = WebInsightPro(url)
    error = tool.fetch_data()

    if error:
        return jsonify({"error": error})

    report = tool.full_report()
    df = tool.get_dataframe()

    return jsonify({
        "report": report,
        "data": df.to_dict(orient='records')
    })

if __name__ == '__main__':
    app.run(debug=True)
