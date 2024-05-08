import threading
import yfinance as yf
import random

class YahooFinancePriceWorker(threading.Thread):
    def __init__(self,symbol, **kwargs):
        super(YahooFinancePriceWorker, self).__init__(**kwargs)
        self._symbol = symbol
        self_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=5min&apikey=F4W8MV5EP14PMZ9S"
        self.start()




    def run(self):
        data = yf.Ticker(self._symbol)
        hist = data.history(period="1mo", interval="1d")
        if not hist.empty:
            last_date = hist.index.max() 
            last_close_price = hist.loc[last_date, 'Close'] 
            print(f"Last closing price for {self._symbol} on {last_date.date()} is: {last_close_price}")
        else:
            print(f"No data available for {self._symbol}")

