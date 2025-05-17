from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
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

    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "ul.pagination"))
    )

    try:
        last_page_link = driver.find_element(By.CSS_SELECTOR, "li.PagedList-skipToLast a")
        href = last_page_link.get_attribute("href")

        # Extract the page number from the href using regex
        match = re.search(r'page=(\d+)', href)
        if match:
            return int(match.group(1))
        else:
            return 1
    except:
        return 1



def scrape_books(driver, category_url, category_name, db_cursor, one_page_categories):
    pages_to_visit = []

    if category_name in one_page_categories:
        pages_to_visit = [category_url]
    else:
        last_page = get_last_page(driver, category_url)
        print(f"{category_name}: Last page is {last_page}")
        pages_to_visit = [f"{category_url}?page={page_num}" for page_num in range(1, last_page + 1)]

        
    for page_url in pages_to_visit:
        driver.get(page_url)
        print(f"Visiting: {page_url}")

        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".col-sm-6.col-md-3"))
            )
        except TimeoutException:
            print(f"Timeout while waiting for books on: {page_url}")
            continue

        books = driver.find_elements(By.CSS_SELECTOR, 'div.col-sm-6.col-md-3')

        for book in books:
            try:
                rows = book.find_elements(By.CSS_SELECTOR, '.row')

                # Title
                title = rows[1].find_element(By.CSS_SELECTOR, 'a').text.strip()

                # Author
                author = rows[2].text.strip()

                category = category_name

                # Price row (fifth .row block)
                price_spans = rows[4].find_elements(By.TAG_NAME, 'span')
                real_price = price_spans[2].text.strip()     # e.g. "4999"
                sale_price = price_spans[3].text.strip()         # e.g. "3999 Мкд."

                real_price_numeric = int(''.join(filter(str.isdigit, real_price)))
                sale_price_numeric = int(''.join(filter(str.isdigit, sale_price)))
                sale = real_price_numeric != sale_price_numeric

            except Exception as e:
                title = "N/A"
                author = "N/A"
                real_price = "N/A"
                sale_price = "N/A"
                sale = False
                print(f"Error extracting book data: {e}")
            
            retrieved_at = datetime.now().date()
            
            db_cursor.execute(''' 
                    INSERT INTO akademskakniga_books (title, author, real_price, sale_price, sale, category, retrieved_at) 
                    VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (title, author, real_price, sale_price, sale, category, retrieved_at))

            time.sleep(2)

def export_db_to_csv(db_cursor, folder="akademskakniga.mk", filename="akademska_books.csv"):
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, filename)

    db_cursor.execute("SELECT title, author, real_price, sale_price, sale, category, retrieved_at FROM akademskakniga_books")
    rows = db_cursor.fetchall()

    with open(filepath, mode="w", newline='', encoding="utf-8-sig") as file:
        writer = csv.writer(file)
        writer.writerow(["Title", "Author", "Real Price", "Sale Price", "Sale", "Category",  "Retrieved At"])
        writer.writerows(rows)



def create_database():
    conn = sqlite3.connect('akademskakniga_books.db')
    cursor = conn.cursor()


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
    return conn, cursor

def main():

    urls = [
    ("https://akademskakniga.mk/BooksM/BooksPoSubCat/1", "Accounting & Finance"),
    ("https://akademskakniga.mk/BooksM/BooksPoSubCat/2", "Agriculture"),
    ("https://akademskakniga.mk/BooksM/BooksPoSubCat/3", "Architecture & Design"),
    ("https://akademskakniga.mk/BooksM/BooksPoSubCat/4", "Arts"),
    ("https://akademskakniga.mk/BooksM/BooksPoSubCat/755", "Biographies"),
    ("https://akademskakniga.mk/BooksM/BooksPoSubCat/5", "Business & Management"),
    ("https://akademskakniga.mk/BooksM/BooksPoSubCat/722", "Celebrities"),
    ("https://akademskakniga.mk/BooksM/BooksPoSubCat/6", "Chemistry"),
    ("https://akademskakniga.mk/BooksM/BooksPoSubCat/677", "Children's Corner"),
    ("https://akademskakniga.mk/BooksM/BooksPoSubCat/7", "Computing"),
    ("https://akademskakniga.mk/BooksM/BooksPoSubCat/698", "Crime & Thriller"),
    ("https://akademskakniga.mk/BooksM/BooksPoSubCat/8", "Culinary & Hospitality"),
    ("https://akademskakniga.mk/BooksM/BooksPoSubCat/24", "Dictionaries & Thesauri"),
    ("https://akademskakniga.mk/BooksM/BooksPoSubCat/9", "Economics"),
    ("https://akademskakniga.mk/BooksM/BooksPoSubCat/10", "Education"),
    ("https://akademskakniga.mk/BooksM/BooksPoSubCat/642", "Encyclopedies & Travel guides"),
    ("https://akademskakniga.mk/BooksM/BooksPoSubCat/11", "Engineering & Materials Science"),
    ("https://akademskakniga.mk/BooksM/BooksPoSubCat/12", "Geography, Geology & Environmental Sciences"),
    ("https://akademskakniga.mk/BooksM/BooksPoSubCat/699", "Graphic Novels, Anime & Manga"),
    ("https://akademskakniga.mk/BooksM/BooksPoSubCat/633", "History"),
    ("https://akademskakniga.mk/BooksM/BooksPoSubCat/13", "Humanities"),
    ("https://akademskakniga.mk/BooksM/BooksPoSubCat/14", "Law & Criminology"),
    ("https://akademskakniga.mk/BooksM/BooksPoSubCat/15", "Life Sciences"),
    ("https://akademskakniga.mk/BooksM/BooksPoSubCat/646", "Linguistics"),
    ("https://akademskakniga.mk/BooksM/BooksPoSubCat/618", "Literature"),
    ("https://akademskakniga.mk/BooksM/BooksPoSubCat/16", "Mathematics & Statistics"),
    ("https://akademskakniga.mk/BooksM/BooksPoSubCat/17", "Medicine, Nursing & Dentistry"),
    ("https://akademskakniga.mk/BooksM/BooksPoSubCat/700", "Pets"),
    ("https://akademskakniga.mk/BooksM/BooksPoSubCat/18", "Physics & Astronomy"),
    ("https://akademskakniga.mk/BooksM/BooksPoSubCat/377", "Political science"),
    ("https://akademskakniga.mk/BooksM/BooksPoSubCat/19", "Psychology"),
    ("https://akademskakniga.mk/BooksM/BooksPoSubCat/371", "Public relations & Communication studies"),
    ("https://akademskakniga.mk/BooksM/BooksPoSubCat/695", "Science Fiction, Fantasy & Horror"),
    ("https://akademskakniga.mk/BooksM/BooksPoSubCat/20", "Social & Developmental Sciences"),
    ("https://akademskakniga.mk/BooksM/BooksPoSubCat/21", "Sport & Exercise"),
    ("https://akademskakniga.mk/BooksM/BooksPoSubCat/22", "Veterinary Medicine"),
    ("https://akademskakniga.mk/BooksM/BooksPoSubCat/367", "War, Peace & Conflict resolution studies")
    ]

    one_page_categories = {
        "Celebrities",
        "Veterinary Medicine"
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