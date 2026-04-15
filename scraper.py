import requests
from bs4 import BeautifulSoup

class WebInsightPro:
    def __init__(self, url):
        self.url = url
        self.soup = None

    def fetch_data(self):
        try:
            headers = {
                "User-Agent": "Mozilla/5.0"
            }

            res = requests.get(self.url, headers=headers, timeout=10)
            res.raise_for_status()

            self.soup = BeautifulSoup(res.text, "html.parser")
            return None

        except Exception as e:
            return str(e)

    def full_report(self):
        title = self.soup.title.string if self.soup.title else "N/A"

        desc_tag = self.soup.find("meta", attrs={"name": "description"})
        description = desc_tag["content"] if desc_tag else "N/A"

        h1 = len(self.soup.find_all("h1"))
        h2 = len(self.soup.find_all("h2"))
        h3 = len(self.soup.find_all("h3"))

        links = self.soup.find_all("a")
        internal = 0
        external = 0

        for link in links:
            href = link.get("href")
            if href:
                if self.url in href:
                    internal += 1
                else:
                    external += 1

        # SEO score بسيط
        score = 50
        if title != "N/A":
            score += 10
        if description != "N/A":
            score += 10
        if h1 > 0:
            score += 10
        if internal > 0:
            score += 10

        suggestions = []
        if description == "N/A":
            suggestions.append("Add meta description")
        if h1 == 0:
            suggestions.append("Add H1 tag")
        if internal == 0:
            suggestions.append("Add internal links")

        return {
            "seo_score": score,
            "meta": {
                "title": title,
                "description": description
            },
            "headings": {
                "h1": h1,
                "h2": h2,
                "h3": h3
            },
            "links": {
                "internal": internal,
                "external": external
            },
            "suggestions": suggestions
        }
