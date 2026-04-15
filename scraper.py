import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def analyze_site(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        res = requests.get(url, headers=headers, timeout=10)
    except:
        return {"error": "فشل الاتصال بالموقع"}

    if res.status_code != 200:
        return {"error": "الموقع لا يستجيب"}

    soup = BeautifulSoup(res.text, "html.parser")

    score = 0
    suggestions = []

    # ---------------- TITLE ----------------
    title = soup.title.string.strip() if soup.title else ""

    if title:
        score += 20
        if 30 <= len(title) <= 60:
            score += 10
        else:
            suggestions.append("حسّن طول العنوان (30-60 حرف)")
    else:
        suggestions.append("أضف عنوان للصفحة (Meta Title)")

    # ---------------- DESCRIPTION ----------------
    desc_tag = soup.find("meta", attrs={"name": "description"})
    description = desc_tag["content"].strip() if desc_tag and desc_tag.get("content") else ""

    if description:
        score += 20
        if 50 <= len(description) <= 160:
            score += 10
        else:
            suggestions.append("الوصف لازم يكون بين 50-160 حرف")
    else:
        suggestions.append("أضف Meta Description")

    # ---------------- HEADINGS ----------------
    h1_tags = soup.find_all("h1")
    h2_tags = soup.find_all("h2")
    h3_tags = soup.find_all("h3")

    h1 = len(h1_tags)
    h2 = len(h2_tags)
    h3 = len(h3_tags)

    if h1 == 1:
        score += 15
    elif h1 > 1:
        score += 5
        suggestions.append("يفضل يكون H1 واحد فقط")
    else:
        suggestions.append("أضف H1")

    if h2 > 0:
        score += 10
    else:
        suggestions.append("أضف H2 لتحسين الهيكلة")

    # ---------------- LINKS ----------------
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

    if internal > 0:
        score += 10
    else:
        suggestions.append("أضف روابط داخلية")

    if external > 0:
        score += 5

    # ---------------- IMAGES (ALT) ----------------
    images = soup.find_all("img")
    missing_alt = 0

    for img in images:
        if not img.get("alt"):
            missing_alt += 1

    if len(images) > 0:
        if missing_alt == 0:
            score += 10
        else:
            suggestions.append("بعض الصور بدون alt text")

    # ---------------- FINAL ----------------
    if score > 100:
        score = 100

    return {
        "title": title or "N/A",
        "description": description or "N/A",
        "h1": h1,
        "h2": h2,
        "h3": h3,
        "internal_links": internal,
        "external_links": external,
        "images": len(images),
        "missing_alt": missing_alt,
        "score": score,
        "suggestions": suggestions
    }
