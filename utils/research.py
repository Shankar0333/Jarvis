import requests
from bs4 import BeautifulSoup
import re

class ResearchTools:
    @staticmethod
    def autonomous_search(query: str) -> str:
        """
        Searches the web and extracts the most relevant text content.
        Args:
            query: The search query.
        """
        try:
            # Use a simple search engine scrap (or a real API in production)
            url = f"https://www.google.com/search?q={query}"
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, "html.parser")

            # Extract links
            links = []
            for link in soup.find_all("a"):
                href = link.get("href")
                if href and "/url?q=" in href:
                    clean_link = re.search(r"/url\?q=(.*?)&", href).group(1)
                    if "google.com" not in clean_link:
                        links.append(clean_link)

            if not links:
                return f"I couldn't find any direct results for {query}, Sir."

            # Visit the first relevant link
            target_url = links[0]
            res = requests.get(target_url, headers=headers, timeout=5)
            target_soup = BeautifulSoup(res.text, "html.parser")

            # Extract text
            paragraphs = target_soup.find_all("p")
            content = " ".join([p.text for p in paragraphs[:5]]) # Get first 5 paragraphs
            return f"Research result from {target_url}: {content[:2000]}..."

        except Exception as e:
            return f"My research attempt failed, Sir. Error: {str(e)}"

research_tools_list = [ResearchTools.autonomous_search]
