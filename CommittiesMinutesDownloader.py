import requests 
from dotenv import load_dotenv
import os

load_dotenv()
CONGRESS_API_KEY = os.getenv("CONGRESS_API_KEY")

def download_committee_minutes(pIndex):
    url = f"https://open.assembly.go.kr/portal/openapi/VCONFSPCCONFLIST?ERACO=제21대&Type=json&pIndex={pIndex}&pSize=100&KEY={CONGRESS_API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Error: {response.status_code}")
        return None
    
# def save_committee_minutes(data, filename):
#     if data and 'result' in data and 'items' in data['result']:
#         items = data['VCONFSPCCONFLIST'][2]["row"]
#         with open(filename, 'w', encoding='utf-8') as file:
#             for item in items:
#                 file.write(f"{item}\n")
#     else:
#         print("No data to save or data format is incorrect.")

if __name__ == "__main__":
    pIndex = 1  # 페이지 인덱스 설정
    committee_minutes = download_committee_minutes(pIndex)
    
    print(committee_minutes)