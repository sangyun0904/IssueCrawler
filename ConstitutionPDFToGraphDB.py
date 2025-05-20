import os
import fitz 
import psycopg2
from neo4j import GraphDatabase
from dotenv import load_dotenv
import re

load_dotenv() 

NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
CONSTITUTION_PDF_PATH = "대한민국 헌법.pdf"

URI = "bolt://localhost:7687"

def get_connection():
    conn = psycopg2.connect(
        host=os.getenv("POSTGRESDB_HOST"),
        database=os.getenv("POSTGRESDB_DEBATE_NAME"),
        user=os.getenv("POSTGRESDB_USER"),
        password=os.getenv("POSTGRESDB_PASSWORD")
    )
    return conn

if __name__ == "__main__":
    doc = fitz.open(CONSTITUTION_PDF_PATH)

    conn = get_connection()
    cursor = conn.cursor()

    count = 1
    lawId = None
    for page in doc:
        isJunmoon = False
        sectionNum = 1
        sectionId = None
        articleNum = 1 
        clauseNum = 1
        content = ""

        if count > 4:
            break
        
        print(f"Page {count} text:")
        text = page.get_text()
        for line in text.split('\n'):
            if re.search("전문", line):
                isJunmoon = True
                continue

            if re.search("제\d+장", line):
                if isJunmoon:
                    lo = conn.lobject(0, 'w', 0)
                    lo.write(content.encode('utf-8'))
                    cursor.execute("""
                        INSERT INTO laws (
                            title, description
                        ) VALUES ('대한민국 헌법', %s) 
                        RETURNING id
                    """, (lo.oid,))
                    lawId = cursor.fetchone()[0]
                    isJunmoon = False
                    content = ""
                
                cursor.execute("""
                    INSERT INTO law_sections (
                        law_id, section_num, section_title
                    ) VALUES (%s, %s, %s)
                    RETURNING id
                    """, (lawId, sectionNum, re.sub(r"제\d+장 ", "", line)))
                sectionId = cursor.fetchone()[0]
                sectionNum += 1
                continue
                
            if re.search("제\d+조", line):
                if content != "":
                    lo = conn.lobject(0, 'w', 0)
                    lo.write(content.encode('utf-8'))
                    cursor.execute("""
                        INSERT INTO law_articles (
                            section_id, article_num, clause_num, clause_content
                        ) VALUES (%s, %s, %s, %s)
                        """, (sectionId, articleNum, clauseNum, lo.oid))
                    content = ""

                if re.search("[\u2460-\u2473]", line):
                    clauseNum = ord(re.findall("[\u2460-\u2473]", line)[0]) - 2460 + 1
                    content = re.sub(r"제\d+조 \([\u2460-\u2473]\)", "", line)
                else:
                    clauseNum = 1
                    content = re.sub(r"제\d+조 ", "", line)
                continue

            if re.search("[\u2460-\u2473]", line):
                clauseNum = ord(re.findall("[\u2460-\u2473]", line)[0]) - 2460 + 1
                content = re.sub(r"\([\u2460-\u2473]\)", "", line)
                continue

            if line !="":
                content += line + "\n"

    conn.commit()
    cursor.close()
    conn.close()