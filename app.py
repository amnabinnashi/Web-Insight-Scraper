from flask import Flask, request, jsonify, send_from_directory
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

app = Flask(__name__)

@app.route("/")
def home():
    return send_from_directory(".", "index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    url = data.get("url")

    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        res = requests.get(url, headers=headers, timeout=10)
    except:
        return jsonify({"error": "فشل الاتصال"})

    soup = BeautifulSoup(res.text, "html.parser")

    title = soup.title.string if soup.title else "N/A"

    desc_tag = soup.find("meta", attrs={"name": "description"})
    description = desc_tag["content"] if desc_tag and desc_tag.get("content") else "N/A"

    h1 = len(soup.find_all("h1"))
    h2 = len(soup.find_all("h2"))
    h3 = len(soup.find_all("h3"))

    links = soup.find_all("a")
    internal = 0
    external = 0

    domain = urlparse(url).netloc

    for link in links:
        href = link.get("href")
        if href:
            if domain in href:
                internal += 1
            elif href.startswith("http"):
                external += 1

    score = 50 + (h1 * 5) + (h2 * 3)

    suggestions = []
    if h1 == 0:
        suggestions.append("أضف H1")
    if description == "N/A":
        suggestions.append("أضف Meta Description")

    return jsonify({
        "title": title,
        "description": description,
        "h1": h1,
        "h2": h2,
        "h3": h3,
        "internal_links": internal,
        "external_links": external,
        "score": score,
        "suggestions": suggestions
    })


if __name__ == "__main__":
    app.run(debug=True)
