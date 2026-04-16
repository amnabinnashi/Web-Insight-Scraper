from flask import Flask, request, jsonify, send_from_directory
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import os

app = Flask(__name__)

# ---------------- الصفحة الرئيسية ----------------
@app.route("/")
def home():
    return send_from_directory(os.getcwd(), "index.html")


# ---------------- API التحليل ----------------
@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    url = data.get("url")

    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        res = requests.get(url, headers=headers, timeout=10)
    except:
        return jsonify({"error": "فشل الاتصال بالموقع"})

    soup = BeautifulSoup(res.text, "html.parser")

    # TITLE
    title = soup.title.string.strip() if soup.title else "N/A"

    # DESCRIPTION
    desc_tag = soup.find("meta", attrs={"name": "description"})
    description = desc_tag["content"].strip() if desc_tag and desc_tag.get("content") else "N/A"

    # HEADINGS
    h1 = len(soup.find_all("h1"))
    h2 = len(soup.find_all("h2"))
    h3 = len(soup.find_all("h3"))

    # LINKS
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

    # SCORE
    score = 50
    if title != "N/A":
        score += 10
    if description != "N/A":
        score += 10
    if h1 == 1:
        score += 10
    if h2 > 0:
        score += 5
    if internal > 0:
        score += 5

    if score > 100:
        score = 100

    # SUGGESTIONS
    suggestions = []
    if h1 == 0:
        suggestions.append("أضف H1")
    elif h1 > 1:
        suggestions.append("يفضل H1 واحد")

    if description == "N/A":
        suggestions.append("أضف Meta Description")

    if internal == 0:
        suggestions.append("أضف روابط داخلية")

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


# ---------------- تشغيل ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
