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
        EC.presence_of_element_located((By.CSS_SELECTOR, "ul.page-numbers"))
    )

    page_numbers = driver.find_elements(By.CSS_SELECTOR, "ul.page-numbers li a.page-numbers")
    numbered_pages = [el for el in page_numbers if el.text.isdigit()]

    if numbered_pages:
        return int(numbered_pages[-1].text)
    else:
        return 1  

def scrape_books(driver, category_url, category_name, db_cursor):
    last_page = get_last_page(driver, category_url)
    print(f"Scraping category: {category_name}, Last page: {last_page}")

    for page_num in range(1, last_page + 1):
        if page_num == 1:
            page_url = category_url
        else:
            page_url = f"{category_url}page/{page_num}/"
        
        driver.get(page_url)
        print(f"Visiting: {page_url}")

        WebDriverWait(driver, 20).until(
            EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".product"))
        )

        books_on_page = driver.find_elements(By.CSS_SELECTOR, ".product")
        for book in books_on_page:
            try:
                title = book.find_element(By.CSS_SELECTOR, ".book-name").text
            except:
                title = "N/A" 

            try:
                author = book.find_element(By.CSS_SELECTOR, ".book-author").text
            except:
                author = "N/A" 

            try:
                sale_price_el = book.find_element(By.CSS_SELECTOR, ".book-price .price ins .woocommerce-Price-amount")
                real_price_el = book.find_element(By.CSS_SELECTOR, ".book-price .price del .woocommerce-Price-amount")
                sale_price = sale_price_el.text
                real_price = real_price_el.text
                sale = True
            except NoSuchElementException:
                try:
                    # If not on sale, just get regular price
                    price_el = book.find_element(By.CSS_SELECTOR, ".book-price .price .woocommerce-Price-amount")
                    sale_price = real_price = price_el.text
                    sale = False
                except NoSuchElementException:
                    # If no price is available at all
                    sale_price = real_price = "N/A"
                    sale = False

            retrieved_at = datetime.now().date()

            db_cursor.execute(''' 
                INSERT INTO sakamknigi_books (title, author, real_price, sale_price, sale, category, retrieved_at) 
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (title, author, real_price, sale_price, sale, category_name, retrieved_at))

        time.sleep(2)

def create_database():
    conn = sqlite3.connect('sakamknigi_books.db')
    cursor = conn.cursor()


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

    conn.commit()
    return conn, cursor

def export_db_to_csv(db_cursor, folder="sakamknigi.mk", filename="sakam_knigi_books.csv"):
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, filename)

    db_cursor.execute("SELECT title, author, real_price, sale_price, sale, category, retrieved_at FROM books")
    rows = db_cursor.fetchall()

    with open(filepath, mode="w", newline='', encoding="utf-8-sig") as file:
        writer = csv.writer(file)
        writer.writerow(["Title", "Author", "Real Price", "Sale Price", "Sale", "Category",  "Retrieved At"])
        writer.writerows(rows)

def main():

    urls = [
        ("https://sakamknigi.mk/shop/romance/", "Романси"),
        ("https://sakamknigi.mk/shop/horror/", "Трилери"),
        ("https://sakamknigi.mk/shop/mystery/", "Мистерии"),
        ("https://sakamknigi.mk/shop/drama/", "Драми"),
        ("https://sakamknigi.mk/shop/history/", "Историски"),
        ("https://sakamknigi.mk/shop/chick-lit/", "Чик Лит"),
        ("https://sakamknigi.mk/shop/young-adult/", "За млади"),
        ("https://sakamknigi.mk/shop/detski/", "Детски книги"),
        ("https://sakamknigi.mk/shop/non-fiction/", "Психологија"),
        ("https://sakamknigi.mk/shop/duhovni/", "Духовна литература"),
        ("https://sakamknigi.mk/shop/zdrava-hrana/", "Здравје и исхрана")
    ]

    options = get_default_chrome_options()
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    conn, cursor = create_database()

    try:
        for category_url, category_name in urls:
            scrape_books(driver, category_url, category_name, cursor)
        conn.commit()
        export_db_to_csv(cursor)
    finally:
        conn.close()
        driver.quit()

if __name__ == "__main__":
    main()
