import time
from workers.Wikiworkers import Wikiworker
from workers.YahooFInanceWorker import YahooFinancePriceScheduler
from workers.PostgresWorker import PostgresMasterScheduler
from multiprocessing import Queue


def main():
    symbol_queue = Queue()
    postgres_queue = Queue()
    scrapper_start_time = time.time()

    wikiWorker = Wikiworker()
    yahoo_finance_price_scheduler_thread = []
    num_yahoo_finance_workers = 4

    for i in range(num_yahoo_finance_workers):
        yahooFinancePriceScheduler = YahooFinancePriceScheduler(input_queue=symbol_queue, output_queue=postgres_queue)
        yahoo_finance_price_scheduler_thread.append(yahooFinancePriceScheduler)


    postgres_scheduler_thread = []
    num_postgres_workers = 2

    for i in range(num_postgres_workers):
        postgresScheduler = PostgresMasterScheduler(input_queue=postgres_queue)
        postgres_scheduler_thread.append(postgresScheduler)

    for symbol in wikiWorker.get_sp_500_companies():
        symbol_queue.put(symbol)

    for _ in range(len(yahoo_finance_price_scheduler_thread)):
        symbol_queue.put("DONE")

    for thread in range(len(yahoo_finance_price_scheduler_thread)):
        yahoo_finance_price_scheduler_thread[thread].join()

  

    
    print(f"Extracting time took {round(time.time() - scrapper_start_time, 1)}")



if __name__ == '__main__':
    main()
