import yfinance as yf
import requests

class FinanceNewsTools:
    @staticmethod
    def get_stock_price(ticker: str) -> str:
        """Fetches the latest stock price for a given ticker."""
        try:
            stock = yf.Ticker(ticker)
            price = stock.fast_info['last_price']
            currency = stock.fast_info['currency']
            return f"The current price for {ticker} is {price:.2f} {currency}, Sir."
        except Exception as e:
            return f"I couldn't fetch the data for {ticker}, Sir. Error: {str(e)}"

    @staticmethod
    def get_latest_news(category: str = "general") -> str:
        """Fetches top news headlines."""
        try:
            # Using a public RSS feed or similar simple method
            url = f"https://news.google.com/rss/search?q={category}&hl=en-US&gl=US&ceid=US:en"
            response = requests.get(url)
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(response.text, "xml")
            items = soup.find_all("item")[:5]
            headlines = [f"- {item.title.text}" for item in items]
            return f"Here are the latest {category} headlines, Sir:\n" + "\n".join(headlines)
        except Exception as e:
            return f"I failed to retrieve the news, Sir. Error: {str(e)}"

finance_news_tools_list = [FinanceNewsTools.get_stock_price, FinanceNewsTools.get_latest_news]
