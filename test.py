from sqlalchemy import create_engine, text

# Explicitly start and commit transactions
engine = create_engine('postgresql://postgres:"Password"@localhost:5432/postgres', echo=True, future=True)

with engine.connect() as conn:
    transaction = conn.begin()
    try:
        conn.execute(text("INSERT INTO prices (symbol, price, insert_time) VALUES (:symbol, :price, :insert_time)"),
                     {'symbol': 'TEST', 'price': 123.45, 'insert_time': '2023-05-10 12:00:00'})
        transaction.commit()
        print("Insert successful.")
    except Exception as e:
        transaction.rollback()
        print(f"Error during database operation: {e}")
