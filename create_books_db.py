import sqlite3
import os
import shutil
import csv
def create_books_db():
    os.makedirs("data", exist_ok=True)
    merged_db_path = os.path.join("data", "books.db")
    
    conn = sqlite3.connect(merged_db_path)
    cursor = conn.cursor()

    cursor.execute(''' 
        
        CREATE TABLE IF NOT EXISTS ikona_books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT,
            real_price TEXT,
            sale_price TEXT,
            sale BOOLEAN NOT NULL DEFAULT 0,
            category TEXT NOT NULL,
            retrieved_at DATE
        )
    ''')

    cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS literatura_books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT,
                price TEXT,
                category TEXT NOT NULL,
                retrieved_at DATE
            )
        ''')
    
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS sakamknigi_books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT,
            real_price TEXT,
            sale_price TEXT,
            sale BOOLEAN NOT NULL DEFAULT 0,
            category TEXT NOT NULL,
            retrieved_at DATE
        )
    ''')

    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS akademskakniga_books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT,
            real_price TEXT,
            sale_price TEXT,
            sale BOOLEAN NOT NULL DEFAULT 0,
            category TEXT NOT NULL,
            retrieved_at DATE
        )
    ''')


    conn.commit()
    return conn

def copy_data(source_db_path, source_table, target_conn, target_table):
    source_conn = sqlite3.connect(source_db_path)
    source_cursor = source_conn.cursor()

    target_cursor = target_conn.cursor()

    if target_table == 'literatura_books':
        source_cursor.execute(f"SELECT title, author, price, category, retrieved_at FROM {source_table}")
        rows = source_cursor.fetchall()
        target_cursor.executemany(
            f'''INSERT INTO {target_table} (title, author, price, category, retrieved_at) 
                VALUES (?, ?, ?, ?, ?)''',
            rows
        )
    else:
        source_cursor.execute(f"SELECT title, author, real_price, sale_price, sale, category, retrieved_at FROM {source_table}")
        rows = source_cursor.fetchall()
        target_cursor.executemany(
            f'''INSERT INTO {target_table} (title, author, real_price, sale_price, sale, category, retrieved_at) 
                VALUES (?, ?, ?, ?, ?, ?, ?)''',
            rows
        )

    target_conn.commit()
    source_conn.close()



def export_table_to_csv(db_conn, table_name, csv_path):
    cursor = db_conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()

    col_names = [description[0] for description in cursor.description]

    with open(csv_path, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(col_names) 
        writer.writerows(rows)


if __name__ == "__main__":
    target_conn = create_books_db()

    copy_data("ikona.mk/ikona_books.db", "ikona_books", target_conn, "ikona_books")
    copy_data("literatura.mk/literatura_books.db", "literatura_books", target_conn, "literatura_books")
    copy_data("sakamknigi.mk/sakamknigi_books.db", "sakamknigi_books", target_conn, "sakamknigi_books")
    copy_data("akademskakniga.mk/akademskakniga_books.db", "akademskakniga_books", target_conn, "akademskakniga_books")

    # export_table_to_csv(target_conn, "ikona_books", os.path.join("data", "ikona_books.csv"))
    # export_table_to_csv(target_conn, "literatura_books", os.path.join("data", "literatura_books.csv"))
    # export_table_to_csv(target_conn, "sakamknigi_books", os.path.join("data", "sakamknigi_books.csv"))
    # export_table_to_csv(target_conn, "akademskakniga_books", os.path.join("data", "akademskakniga_books.csv"))

    target_conn.close()
    print("All data successfully merged into data/books.db")

