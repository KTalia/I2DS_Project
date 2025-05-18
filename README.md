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
├── data/                           
│   ├── original_datasets/     # Raw scraped book datasets
│   ├── preprocessed_datasets/ # Cleaned and processed book datasets       
│   └──  books.db              # SQLite database file
│ 
├── akademskakniga.mk/                           
│   ├── preprocess_akademska.ipynb       
│   └──  akademska_scrape.py
│    
├── literatura.mk/
│   ├── literatura_preprocess.ipynb  
│   └── literatura_scrape.py
│               
├── sakamknigi.mk/
│   ├── preprocess_sakamknigi.ipynb
│   └── sakamknigi_scrape.py
│ 
├── ikona.mk/
│   ├── preprocess_ikona.ipynb
│   └── ikona_scrape.py
└── create_books_db.py          # Script to create the database

            
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
