import threading
from sqlalchemy import create_engine
from sqlalchemy.sql import text
import os



class PostgresMasterScheduler(threading.Thread):
    def __init__(self,input_queue, **kwargs):
        super(PostgresMasterScheduler, self).__init__(**kwargs)
        self._input_queue = input_queue
        self.start()


    def run(self):
        while True:
            val = self._input_queue.get()
            if val == "DONE":
                break

            symbol, price, extracted_time = val
            postgresWorker = Postgres(symbol, price, extracted_time)
            postgresWorker.insert_into_db()



class Postgres:
    def __init__(self, symbol, price, extracted_time):
        self._symbol = symbol
        self._price = price
        self._extracted_time = extracted_time
        self._engine = create_engine('postgresql://postgres:"Password"@localhost:5432/postgres')

    # rest of the class remains the same




    def _create_insert_query(self):
        SQL = """INSERT INTO prices (symbol, price, insert_time) VALUES (:symbol, :price, :insert_time)"""
        return SQL

    

    def insert_into_db(self):
        insert_query = self._create_insert_query()
        with self._engine.connect() as conn:
            conn.execute(text(insert_query), {
                'symbol': self._symbol,
                'price': self._price,
                'insert_time': self._extracted_time  
            })
            conn.commit()  



