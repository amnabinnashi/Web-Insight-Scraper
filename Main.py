import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

class WebInsight:
    """
    A professional tool to extract headings and links from any website 
    and organize them into a structured CSV file.
    """
    
    def __init__(self, url):
        self.url = url
        # Define headers to mimic a real browser visit
        self.headers = {'User-Agent': 'Mozilla/5.0'}
        self.data = []

    def fetch_data(self):
        """Connects to the URL and scrapes heading tags (h1, h2, h3)"""
        try:
            # Sending a GET request to the target website
            response = requests.get(self.url, headers=self.headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Scrape headings and store them with a timestamp
            for tag in ['h1', 'h2', 'h3']:
                for item in soup.find_all(tag):
                    self.data.append({
                        'Tag Type': tag,
                        'Content': item.get_text().strip(),
                        'Scraped At': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
            return True
        except Exception as e:
            print(f"Error accessing the website: {e}")
            return False

    def export_to_csv(self, filename="scraped_data.csv"):
        """Saves the collected data into a CSV file using Pandas"""
        if not self.data:
            print("No data found to export!")
            return
        
        # Convert list to a DataFrame and save it
        df = pd.DataFrame(self.data)
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"✅ Success! {len(df)} records saved to: {filename}")

if __name__ == "__main__":
    # User interaction in the terminal
    target_url = input("Please enter the website URL to analyze: ")
    scraper = WebInsight(target_url)
    
    print("⏳ Fetching data, please wait...")
    if scraper.fetch_data():
        scraper.export_to_csv()
