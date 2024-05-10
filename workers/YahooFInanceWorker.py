import threading
import yfinance as yf
import random
import datetime
from queue import Empty


class YahooFinancePriceScheduler(threading.Thread):
    def __init__(self,input_queue, output_queue, **kwargs):
        super(YahooFinancePriceScheduler, self).__init__(**kwargs)    
        self._input_queue = input_queue
        temp_queue = output_queue
        if type(temp_queue) != list:
            temp_queue = [temp_queue]

        self._output_queues = temp_queue
        self.start()

    def run(self):
        while True:
            try:
                val = self._input_queue.get(timeout = 10)

            except Empty:
                print("Yahoo scheduler queue is blank, stopping")
                break
            if val == 'DONE':
                for _ in self._output_queues:
                    _.put("DONE")
                break
            yahooFinancePriceWorker = YahooFinancePriceWorker(symbol=val)
            price = yahooFinancePriceWorker.get_price()
            for _ in self._output_queues:
                output_values = (val, price, datetime.datetime.utcnow())
                _.put(output_values)



class YahooFinancePriceWorker():
    def __init__(self,symbol):
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

