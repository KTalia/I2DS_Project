import sqlite3
import csv
import os

def export_db_to_csv(db_cursor, folder="sakamknigi.mk", filename="books.csv"):
    # Ensure the folder exists
    os.makedirs(folder, exist_ok=True)
    
    # Construct the full path to the CSV file
    filepath = os.path.join(folder, filename)

    # Query all books from the database
    db_cursor.execute("SELECT title, author, real_price, sale_price, sale, category, retrieved_at FROM sakamknigi_books")
    rows = db_cursor.fetchall()

    # Write the data to a CSV file
    with open(filepath, mode="w", newline='', encoding="utf-8-sig") as file:
        writer = csv.writer(file)
        # Write the header
        writer.writerow(["Title", "Author", "Real Price", "Sale Price", "Sale", "Category", "Retrieved At"])
        # Write the book data
        writer.writerows(rows)

conn = sqlite3.connect('sakamknigi_books.db')
cursor = conn.cursor()
export_db_to_csv(cursor)
conn.close()