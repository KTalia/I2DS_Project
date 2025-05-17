import sqlite3
import os

# Define paths
source_db_path = "ikona_books.db"
destination_dir = "data"
destination_db_path = os.path.join(destination_dir, "books.db")

# Make sure "data" directory exists
os.makedirs(destination_dir, exist_ok=True)

# Connect to source (ikona_books.db) and destination (books.db)
src_conn = sqlite3.connect(source_db_path)
src_cursor = src_conn.cursor()

dst_conn = sqlite3.connect(destination_db_path)
dst_cursor = dst_conn.cursor()

# Ensure destination table exists (same schema as source)
dst_cursor.execute('''
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

# Copy data from source table
src_cursor.execute("SELECT title, author, real_price, sale_price, sale, category, retrieved_at FROM ikona_books")
rows = src_cursor.fetchall()

# Insert into destination table
dst_cursor.executemany('''
    INSERT INTO ikona_books (title, author, real_price, sale_price, sale, category, retrieved_at)
    VALUES (?, ?, ?, ?, ?, ?, ?)
''', rows)

# Commit and close
dst_conn.commit()
src_conn.close()
dst_conn.close()

print(f"Copied {len(rows)} rows from ikona_books.db to data/books.db successfully.")
