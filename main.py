import time
from workers.Wikiworkers import Wikiworker
from workers.YahooFInanceWorker import YahooFinancePriceWorker
from multiprocessing import Queue


def main():
    scrapper_start_time = time.time()

    wikiWorker = Wikiworker()
    current_workers = []

    for symbol in wikiWorker.get_sp_500_companies():
        yahooFinancePriceWorker = YahooFinancePriceWorker(symbol=symbol)
        current_workers.append(yahooFinancePriceWorker)

    for thread in range(len(current_workers)):
        current_workers[thread].join()

    
    print(f"Extracting time took {round(time.time() - scrapper_start_time, 1)}")



if __name__ == '__main__':
    main()
