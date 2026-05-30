import unittest
from utils.finance import FinanceNewsTools

class TestFinance(unittest.TestCase):
    def test_stock_price_fetch(self):
        # We can't easily test real network calls here, but we can check if it handles errors
        result = FinanceNewsTools.get_stock_price("INVALID_TICKER_123")
        self.assertIn("Error", result)

if __name__ == "__main__":
    unittest.main()
