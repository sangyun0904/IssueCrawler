import os
import requests
import psycopg2
from dotenv import load_dotenv

load_dotenv() 

CONGRESS_API_KEY = os.getenv("CONGRESS_API_KEY")

def get_connection():
    conn = psycopg2.connect(
        host=os.getenv("POOSTGRESDB_HOST"),
        database=os.getenv("POSTGRESDB_NAME"),
        user=os.getenv("POSTGRESDB_USER"),
        password=os.getenv("POSTGRESDB_PASSWORD")
    )
    return conn

def create_table(conn):
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mona (
            id SERIAL PRIMARY KEY,
            age int,
            hg_nm VARCHAR(255),
            hj_nm VARCHAR(255),
            eng_nm VARCHAR(255),
            bth_gbn_nm VARCHAR(255),
            bth_date TIMESTAMP,
            job_res_nm VARCHAR(255),
            poly_nm VARCHAR(255),
            orig_nm VARCHAR(255),
            elect_gbn_nm VARCHAR(255),
            cmit_nm VARCHAR(255),
            cmits TEXT,
            reele_gbn_nm VARCHAR(255),
            units TEXT,
            sex_gbn_nm VARCHAR(255),
            tel_no VARCHAR(255),
            e_mail VARCHAR(255),
            homepage VARCHAR(255),
            staff TEXT,
            secretary TEXT,
            secretary2 TEXT,
            mona_cd VARCHAR(255),
            mem_title TEXT,
            assem_addr VARCHAR(255))
    """)

    conn.commit()
    cursor.close()
    print("Table created successfully.")

def insert_data(conn, pIndex):
    conn = get_connection() 

    create_table(conn)

    response = requests.get(f"https://open.assembly.go.kr/portal/openapi/nwvrqwxyaytdsfvhu?Type=json&pIndex={pIndex}&pSize=100&KEY={CONGRESS_API_KEY}")
    data = response.json()["nwvrqwxyaytdsfvhu"]
    if (data[0]["head"][1]["RESULT"]["CODE"] == "INFO-000"):
        cursor = conn.cursor()

        for mona in data[1]["row"]:
                cursor.execute("""
                    INSERT INTO mona (age, hg_nm, hj_nm, eng_nm, bth_gbn_nm, bth_date, job_res_nm, poly_nm, orig_nm, elect_gbn_nm, cmit_nm, cmits, reele_gbn_nm, units, sex_gbn_nm, tel_no, e_mail, homepage, staff, secretary, secretary2, mona_cd, mem_title, assem_addr)
                    VALUES (22, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (
                        mona["HG_NM"], mona["HJ_NM"], mona["ENG_NM"],
                        mona["BTH_GBN_NM"], mona["BTH_DATE"], mona["JOB_RES_NM"], mona["POLY_NM"],
                        mona["ORIG_NM"], mona["ELECT_GBN_NM"],
                        mona["CMIT_NM"], mona["CMITS"],
                        mona["REELE_GBN_NM"],
                        mona["UNITS"], mona["SEX_GBN_NM"],
                        mona["TEL_NO"], mona["E_MAIL"],
                        mona["HOMEPAGE"], mona["STAFF"],
                        mona["SECRETARY"], mona["SECRETARY2"],
                        mona["MONA_CD"], mona["MEM_TITLE"],
                        mona["ASSEM_ADDR"]
                    ))
    conn.commit()
    cursor.close()
    conn.close()
    print("Data inserted successfully.")
    return data[0]["head"][0]["list_total_count"]

if __name__ == "__main__":  
    pIndex = 1 
    totoal_mona_count = 1 

    while totoal_mona_count >= pIndex:
        print(f"Processing page {pIndex}...")
        totoal_mona_count = insert_data(get_connection(), pIndex)
        if (totoal_mona_count % 100) == 0:
            totoal_mona_count = totoal_mona_count // 100
        else:
            totoal_mona_count = totoal_mona_count // 100 + 1
            
        pIndex += 1 
