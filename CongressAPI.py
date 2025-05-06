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
    # Create a cursor object
    cursor = conn.cursor()

    # Create a table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS proposed_bill (
            id SERIAL PRIMARY KEY,
            bill_id VARCHAR(255),
            bill_no VARCHAR(255),
            bill_name VARCHAR(255),
            committee VARCHAR(255),
            propose_dt TIMESTAMP,
            proc_result VARCHAR(255),
            age int,
            detail_link VARCHAR(1000),
            proposer VARCHAR(255),
            member_list VARCHAR(1000),
            law_proc_dt TIMESTAMP,
            law_present_dt TIMESTAMP,
            law_submit_dt TIMESTAMP,
            cmt_proc_result_cd VARCHAR(255),
            cmt_proc_dt TIMESTAMP,
            cmt_present_dt TIMESTAMP,
            committee_dt TIMESTAMP,
            proc_dt TIMESTAMP,
            committee_id VARCHAR(255),
            publ_proposer VARCHAR(3000),
            law_proc_result_cd VARCHAR(255),
            rst_proposer VARCHAR(255)
        )
    """)

    # Commit the changes and close the connection
    conn.commit()
    cursor.close()
    print("Table created successfully.")

def insert_data(conn, pIndex):
    conn = get_connection()

    create_table(conn)

    response = requests.get(f'https://open.assembly.go.kr/portal/openapi/nzmimeepazxkubdpn?AGE=21&pIndex={pIndex}&pSize=1000&Type=json&KEY={CONGRESS_API_KEY}')
    data = response.json()["nzmimeepazxkubdpn"]
    if (data[0]["head"][1]["RESULT"]["CODE"] == "INFO-000"):
        cursor = conn.cursor()

        for bill in data[1]["row"]:
            cursor.execute("""
                INSERT INTO proposed_bill (
                    bill_id, bill_no, bill_name, committee, propose_dt, proc_result, age,
                    detail_link, proposer, member_list, law_proc_dt, law_present_dt,
                    law_submit_dt, cmt_proc_result_cd,
                    cmt_proc_dt, cmt_present_dt, committee_dt, proc_dt,
                    committee_id, publ_proposer, law_proc_result_cd,
                    rst_proposer
                ) VALUES (%s, %s, %s, %s, %s, %s,
                          %s, %s, %s, %s, %s,
                          %s, %s, %s,
                          %s, %s, %s, %s,
                          %s, %s, %s,
                          %s)
            """, (
                bill["BILL_ID"], bill["BILL_NO"], bill["BILL_NAME"], bill["COMMITTEE"],
                bill["PROPOSE_DT"], bill["PROC_RESULT"], bill["AGE"],
                bill["DETAIL_LINK"], bill["PROPOSER"], bill["MEMBER_LIST"],
                bill["LAW_PROC_DT"], bill["LAW_PRESENT_DT"],
                bill["LAW_SUBMIT_DT"],
                bill["CMT_PROC_RESULT_CD"],
                bill["CMT_PROC_DT"], bill["CMT_PRESENT_DT"],
                bill["COMMITTEE_DT"], bill["PROC_DT"],
                bill["COMMITTEE_ID"], bill["PUBL_PROPOSER"],
                bill["LAW_PROC_RESULT_CD"],
                bill["RST_PROPOSER"]
            ))

    conn.commit()
    cursor.close()
    conn.close()
    print("Data inserted successfully.")
    return data[0]["head"][0]["list_total_count"]

if __name__ == "__main__":
    pIndex = 1
    total_bills_count = 1

    while total_bills_count > pIndex: 
        print(f"Processing page {pIndex}...")
        pIndex += 1
        total_bills_count = insert_data(get_connection(), pIndex)
        if (total_bills_count % 1000) == 0:
            total_bills_count = total_bills_count // 1000
        else:
            total_bills_count = (total_bills_count // 1000) + 1
