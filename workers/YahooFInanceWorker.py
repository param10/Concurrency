import threading
import yfinance as yf
import random
import datetime


class YahooFinancePriceScheduler(threading.Thread):
    def __init__(self,input_queue,output_queue, **kwargs):
        super(YahooFinancePriceScheduler, self).__init__(**kwargs)    
        self._input_queue = input_queue
        self._output_queue = output_queue
        self.start()

    def run(self):
        while True:
            val = self._input_queue.get()
            if val == 'DONE':
                if self._output_queue is not None:
                    self._output_queue.put("DONE")
                break
            yahooFinancePriceWorker = YahooFinancePriceWorker(symbol=val)
            price = yahooFinancePriceWorker.get_price()
            if self._output_queue is not None:
                output_values = (val, price, datetime.datetime.utcnow())
                self._output_queue.put(output_values)



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

