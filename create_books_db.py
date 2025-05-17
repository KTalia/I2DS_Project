import pandas as pd
import sqlite3

conn = sqlite3.connect("books.db")

# Load datasets
df_lit = pd.read_csv("literatura.mk/literatura_books.csv")
df_sakam = pd.read_csv("sakamknigi.mk/sakamknigi_books.csv")
df_aka = pd.read_csv("akademskakniga.mk/akademska_books.csv")

# Write each dataframe to its own table
df_lit.to_sql('literatura', conn, if_exists='replace', index=False)
df_sakam.to_sql('sakamknigi', conn, if_exists='replace', index=False)
df_aka.to_sql('akademska', conn, if_exists='replace', index=False)

conn.close()
