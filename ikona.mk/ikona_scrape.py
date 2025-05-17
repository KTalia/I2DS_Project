from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import sqlite3
import csv
import time
import os
import re

def get_default_chrome_options():
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--headless")
    options.add_argument("--disable-dev-shm-usage")
    return options

def get_last_page(driver, base_url):
    driver.get(base_url)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "ul.page-numbers"))
    )

    try:
        page_elements = driver.find_elements(By.CSS_SELECTOR, "ul.page-numbers li a.page-numbers")
        page_numbers = []

        for el in page_elements:
            try:
                page_numbers.append(int(el.text))
            except ValueError:
                continue  # Skip non-numeric elements like "→"

        if page_numbers:
            return max(page_numbers)
        else:
            return 1
    except Exception:
        return 1

def export_db_to_csv(db_cursor, folder="ikona.mk", filename="ikona_books.csv"):
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, filename)

    db_cursor.execute("SELECT title, author, real_price, sale_price, sale, category, retrieved_at FROM ikona_books")
    rows = db_cursor.fetchall()

    with open(filepath, mode="w", newline='', encoding="utf-8-sig") as file:
        writer = csv.writer(file)
        writer.writerow(["Title", "Author", "Real Price", "Sale Price", "Sale", "Category",  "Retrieved At"])
        writer.writerows(rows)

def create_database():
    conn = sqlite3.connect('ikona_books.db')
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

    conn.commit()
    return conn, cursor

def scrape_books(driver, category_url, category_name, db_cursor, one_page_categories):
    pages_to_visit = []

    if category_name in one_page_categories:
        pages_to_visit = [category_url]
    else:
        last_page = get_last_page(driver, category_url)
        print(f"{category_name}: Last page is {last_page}")
        pages_to_visit = [f"{category_url}?product-page={page_num}" for page_num in range(1, last_page + 1)]

    for page_url in pages_to_visit:
        driver.get(page_url)
        print(f"Visiting: {page_url}")
        time.sleep(2) 

        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li.product a.woocommerce-LoopProduct-link"))
            )
        except TimeoutException:
            print(f"Timeout while waiting for books on: {page_url}")
            continue

        # Get all book links on the page
        book_elements = driver.find_elements(By.CSS_SELECTOR, "li.product a.woocommerce-LoopProduct-link")
        book_links = [book.get_attribute("href") for book in book_elements]

        for link in book_links:
            driver.get(link)
            time.sleep(1) 

            try:
                title = driver.find_element(By.TAG_NAME, "h1").text
            except:
                title = "N/A"

            try:
                author = driver.find_element(By.CSS_SELECTOR, "div.product-attribute-avtor h4 a").text
            except:
                author = "N/A"

            real_price = None
            sale_price = None
            sale = False
            try:
                # Try to get sale prices first
                real_price = driver.find_element(By.CSS_SELECTOR, "p.price del span.woocommerce-Price-amount").text
                sale_price = driver.find_element(By.CSS_SELECTOR, "p.price ins span.woocommerce-Price-amount").text
                sale = True
            except:
                try:
                    real_price = driver.find_element(By.CSS_SELECTOR, "p.price span.woocommerce-Price-amount").text
                    sale_price = None
                    sale = False
                except:
                    real_price = "N/A"
                    sale_price = None
                    sale = False

            retrieved_at = datetime.now().date()

            # Insert into DB without the URL column
            insert_query = """
                INSERT INTO ikona_books (title, author, real_price, sale_price, sale, category, retrieved_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """
            db_cursor.execute(insert_query, (title, author, real_price, sale_price, sale, category_name, retrieved_at))


            time.sleep(2)

def main():

    urls = [
        ("https://ikona.mk/product-category/beletristika/","Белетристика"),
        ("https://ikona.mk/product-category/romansa/","Романса"),
        ("https://ikona.mk/product-category/klasici-i-sovremeni-klasici/","Класики и современи класики"),
        ("https://ikona.mk/product-category/teenage/","Тинејџ"),
        ("https://ikona.mk/product-category/umetnost-i-arhitektura/","Уметност и архитектура"),
        ("https://ikona.mk/product-category/ekonomija/","Економија"),
        ("https://ikona.mk/product-category/istorija-i-politika/","Историја и политика"),
        ("https://ikona.mk/product-category/popularna-psihologija/","Популарна психологија"),
        ("https://ikona.mk/product-category/hristijanstvo/","Христијанство"),
        ("https://ikona.mk/product-category/semejstvo-i-zdrav-zivot/","Семејство и здрав живот"),
        ("https://ikona.mk/product-category/filosofija/","Филозофија"),
        ("https://ikona.mk/product-category/detsko-katce/detski/","Детски"),
        ("https://ikona.mk/product-category/ikoni/?product-page=2","Икони") 
    ]

    one_page_categories = {
        "Уметност и архитектура",
        "Филозофија"
    }
    
    options = get_default_chrome_options()
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    conn, cursor = create_database()

    try:
        for category_url, category_name in urls:
            scrape_books(driver, category_url, category_name, cursor, one_page_categories)
        conn.commit()
        export_db_to_csv(cursor)
    finally:
        conn.close()
        driver.quit()

if __name__ == "__main__":
    main()