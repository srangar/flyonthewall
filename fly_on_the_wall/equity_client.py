import yfinance as yf


class EquityClient:
    def __init__(self, ticker: str):
        self.ticker = ticker
        self.yfinance_ticker = yf.Ticker(ticker)

    def get_current_price(self) -> str:
        todays_data = self.yfinance_ticker.history(period="1d")
        return todays_data["Close"][0]

    def get_opening_price(self) -> str:
        opening_price = self.yfinance_ticker.get_info()["open"]
        return opening_price

    def get_delta(self) -> float:
        open_price = self.get_opening_price()
        price_diff = open_price - float(self.get_current_price())

        return float(price_diff / open_price)
