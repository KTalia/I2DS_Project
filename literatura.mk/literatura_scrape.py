from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import sqlite3
import csv
import time
import os

def get_default_chrome_options():
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--headless")
    options.add_argument("--disable-dev-shm-usage")
    return options

def get_last_page(driver, base_url):
    driver.get(base_url)

    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "ul.pagination"))
    )

    try:
        last_page_el = driver.find_element(By.CSS_SELECTOR, 'ul.pagination li a[rel="last"]')
        return int(last_page_el.text)
    except Exception:
        return 1


def create_database():
    # os.makedirs("literatura.mk", exist_ok=True)

    # db_path = os.path.join("literatura.mk", "literatura_books.db")

    # conn = sqlite3.connect(db_path)
    # cursor = conn.cursor()

    db_path = os.path.join("data", "books.db")

    os.makedirs("data", exist_ok=True)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

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

    conn.commit()
    return conn, cursor


def scrape_books(driver, base_url, db_cursor):
    last_page = get_last_page(driver, base_url)

    book_data = []
    for i in range(1, last_page):
        url = base_url if i == 1 else f"{base_url}page-{i}"
        driver.get(url)

    
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.item-data.col-xs-12.col-sm-12"))
        ) 

        books = driver.find_elements(By.CSS_SELECTOR, "div.item-data.col-xs-12.col-sm-12")

        for book in books:
            try:
                title_div = book.find_element(By.CLASS_NAME, "title")
                title = title_div.find_element(By.TAG_NAME, "a").text.strip()

                try:
                    author = book.find_element(By.CSS_SELECTOR, ".atributs-wrapper .value").text.strip()
                except NoSuchElementException:
                    author = "N/A"

                price_element = book.find_element(By.CSS_SELECTOR, ".prices-wrapper .current-price")
                clean_price = price_element.text.replace("МКД", "").strip()

                category = book.find_element(By.CSS_SELECTOR, ".category-wrapper .category").text.strip()
                retrieved_at = datetime.now().date()

                book_data.append({
                    "Title": title,
                    "Author": author,
                    "Price": clean_price,
                    "Category": category,
                    "Retrieved at": retrieved_at
                })

                db_cursor.execute(
                    '''
                    INSERT INTO literatura_books (title, author, price, category, retrieved_at) 
                    VALUES (?, ?, ?, ?, ?)
                    ''',
                    (title, author, clean_price, category, retrieved_at)
                )

            except Exception as e:
                print(f"Error extracting book details: {e}")

   

def export_db_to_csv(db_cursor, folder="../data/original_datasets", filename="literatura_books.csv"):
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, filename)

    db_cursor.execute("SELECT title, author, price, category, retrieved_at FROM literatura_books")
    rows = db_cursor.fetchall()

    with open(filepath, mode="w", newline='', encoding="utf-8-sig") as file:
        writer = csv.writer(file)
        writer.writerow(["Title", "Author", "Price", "Category",  "Retrieved At"])
        writer.writerows(rows)

def main():

    url = "https://www.literatura.mk/knigi/"

    options = get_default_chrome_options()
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    conn, cursor = create_database()

    try:
        scrape_books(driver, url, cursor)
        conn.commit()
        export_db_to_csv(cursor)
    finally:
        conn.close()
        driver.quit()

if __name__ == "__main__":
    main()