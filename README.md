# I2DS_Project: Collecting Data from Multiple Bookstores, Including Preprocessing and Standardization
- This project focuses on the collection, preprocessing, and standardization of product data from four different online bookstores: [Literatura.mk](https://www.literatura.mk/) , [SakamKnigi.mk](https://sakamknigi.mk/shop/) , [AkademskaKniga.mk](https://akademskakniga.mk/)
and  [Ikona.mk](https://ikona.mk/). The goal was to automate the data collection process, clean and organize the extracted information, and prepare it for future analysis or application in other systems.
---
## Technologies Used
- **Python**
- **Libraries and Modules:** – selenium, pandas, numpy, sqlite3, csv, missingno     
- **SQLite** – Relational database to store scraped data efficiently
---
## Project Structure
```
I2DS_Project/
│
├── akademskakniga.mk/                           
│   ├── akademska_books.csv
│   ├── akademska_books.db           
│   ├── preprocess_akademska.ipynb       
│   └──  akademska_scrape.py      
│
├── literatura.mk/
│   ├── literatura_books.csv                     
│   ├── literatura_books.db
│   ├── literatura_preprocess.ipynb  
│   └── literatura_scrape.py              
├── sakamknigi.mk/
│   ├── sakamknigi_books.csv
│   ├── sakamknigi_books.db                     
│   ├── preprocess_sakamknigi.ipynb
│   └── sakamknigi_scrape.py
├── ikona.mk/
│   ├── ikona_books.csv
│   ├── ikona_books.db                     
│   ├── preprocess_ikona.ipynb
│   └── ikona_scrape.py

            
```
---

## 1. Scrape
### 1. SakamKnigi.mk
### 2. Literatura.mk
### 3. AkademskaKniga.mk
### 4. Ikona.mk

## 2. Preprocess / Clean data
### 1. SakamKnigi.mk
### 2. Literatura.mk
### 3. AkademskaKniga.mk
### 4. Ikona.mk
