# I2DS_Project: Collecting Data from Multiple Bookstores, Including Preprocessing and Standardization
- This project focuses on the collection, preprocessing, and standardization of product data from four different online bookstores: [Literatura.mk](https://www.literatura.mk/) , [SakamKnigi.mk](https://sakamknigi.mk/shop/) , [AkademskaKniga.mk](https://akademskakniga.mk/)
and  [Ikona.mk](https://ikona.mk/). The goal was to automate the data collection process, clean and organize the extracted information, and prepare it for future analysis or application in other systems.
- Detailed documentation of the project is available here: [Project Documentation (PDF)](https://github.com/KTalia/I2DS_Project/blob/main/I2DS_Project_Documentation.pdf)
---
## Technologies Used
- **Python**
- **Libraries and Modules:** – selenium, pandas, numpy, sqlite3, csv, missingno     
- **SQLite**
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
│
└── create_books_db.py          # Script to create the database      
```
---
## Bookstore Data Overview and Resources
The following table summarizes the datasets scraped from each bookstore along with links to their respective scraper scripts and Jupyter notebooks for data processing and analysis.

| Bookstore              | Number of Categories | Number of Books Scraped | Number of Discounted Books | Scraper Script                                   | Data Notebook                                    |
|------------------------|----------------------|------------------------|----------------------------|-------------------------------------------------|-------------------------------------------------|
| [Literatura.mk](https://literatura.mk)         | 99                   | 20188                  | 0                          | [literatura_scrape.py](./literatura.mk/literatura_scrape.py)         | [literatura_preprocess.ipynb](./literatura.mk/preprocess_literatura.ipynb)         |
| [AkademskaKniga.mk](https://akademskakniga.mk) | 37                   | 21393                  | 19228                      | [akademska_scrape.py](./akademskakniga.mk/akademska_scrape.py)       | [preprocess_akademska.ipynb](./akademskakniga.mk/preprocess_akademska.ipynb)       |
| [Ikona.mk](https://ikona.mk)                   | 13                   | 1100                   | 32                         | [ikona_scrape.py](./ikona.mk/ikona_scrape.py)                       | [preprocess_ikona.ipynb](./ikona.mk/preprocess_ikona.ipynb)                       |
| [SakamKnigi.mk](https://sakamknigi.mk)         | 11                   | 2167                   | 11                         | [sakamknigi_scrape.py](./sakamknigi.mk/sakamknigi_scrape.py)         | [preprocess_sakamknigi.ipynb](./sakamknigi.mk/preprocess_sakamknigi.ipynb)         |
---
