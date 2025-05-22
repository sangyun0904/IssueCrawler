import os 
import fitz 
import psycopg2 
from dotenv import load_dotenv
import re 

load_dotenv()

COMMITTEE_MINUTES_PDF_PATH = "제22대국회 제422회(임시회) 제1차 보건복지위원회(전체회의) (2025.02.14.).pdf"

def get_connection():
    conn = psycopg2.connect(
        host=os.getenv("POSTGRESDB_HOST"),
        database=os.getenv("POSTGRESDB_COMMITTEE_NAME"),
        user=os.getenv("POSTGRESDB_USER"),
        password=os.getenv("POSTGRESDB_PASSWORD")
    )
    return conn

if __name__ == "__main__":
    doc = fitz.open(COMMITTEE_MINUTES_PDF_PATH)

    conn = get_connection()
    cursor = conn.cursor()

    count = 1
    for page in doc:
        if count > 4:
            break 

        print(f"Page {count} text:")
        text = page.get_text()
        for line in text.split('\n'):
            print(line)
        
        count += 1