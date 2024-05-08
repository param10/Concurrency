import threading
import yfinance as yf
import random


class YahooFinancePriceScheduler(threading.Thread):
    def __init__(self,input_queue, **kwargs):
        super(YahooFinancePriceScheduler, self).__init__(**kwargs)    
        self._input_queue = input_queue
        self.start()

    def run(self):
        while True:
            val = self._input_queue.get()
            if val == 'DONE':
                break
            yahooFinancePriceWorker = YahooFinancePriceWorker(symbol=val)
            price = yahooFinancePriceWorker.get_price()
            print(price)


class YahooFinancePriceWorker():
    def __init__(self,symbol, **kwargs):
        self._symbol = symbol


    def get_price(self):
        data = yf.Ticker(self._symbol)
        hist = data.history(period="1mo", interval="1d")
        if not hist.empty:
            last_date = hist.index.max() 
            last_close_price = hist.loc[last_date, 'Close'] 
            return last_close_price
        else:
            pass

