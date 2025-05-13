import os
import fitz 
from neo4j import GraphDatabase
from dotenv import load_dotenv

load_dotenv() 

NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

URI = "bolt://localhost:7687"

path = "대한민국 헌법.pdf"
doc = fitz.open(path)

count = 1
for page in doc:
    if count > 4:
        break
    
    print(f"Page {count} text:")
    text = page.get_text()
    print(text)

    count += 1