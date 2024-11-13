import requests
import configparser

def load_api_key():
    config = configparser.ConfigParser()
    config.read("application.properties")
    return config.get("DEFAULT", "api_key")

def send_get_request(url):
    headers = {}

    try:
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()
        json_data = response.json()
        return json_data
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

if __name__ == "__main__":
    url = "https://api.nytimes.com/svc/topstories/v2/home.json?api-key=" + load_api_key()
    result = send_get_request(url)

    if result:
        some_data = result.get("someKey")
        print(f"Data from JSON: {some_data}")
    else:
        print("Failed to fetch or parse JSON")
