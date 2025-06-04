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
    
def save_committee_minutes(data):
    urls = []
    if data and 'VCONFSPCCONFLIST' in data and 'row' in data['VCONFSPCCONFLIST'][1]:
        items = data['VCONFSPCCONFLIST'][1]['row']
        for item in items:
            title = "_".join([item['ERACO'], item['CMIT_NM'], item['DGR'], item['CONF_DT']]) + ".pdf"
            file_url = item['DOWN_URL']
            urls.append(file_url)
            save_to_resources(file_url, title)
    else:
        print("No data to save or data format is incorrect.")
    return urls

def save_to_resources(url, file_name):
    resources_dir = "resources"
    os.makedirs(resources_dir, exist_ok=True)  # 폴더가 없으면 생성
    file_path = os.path.join(resources_dir, file_name)

    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"File saved: {file_path}")
    else:
        print(f"Failed to download file from {url}. Status code: {response.status_code}")

if __name__ == "__main__":
    pIndex = 1  # 페이지 인덱스 설정
    committee_minutes = download_committee_minutes(pIndex)
    save_committee_minutes(committee_minutes)