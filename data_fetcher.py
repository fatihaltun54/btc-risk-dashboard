import requests

def get_funding_data():
    url = "https://open-api.coinglass.com/public/v2/funding"
    headers = {
        "accept": "application/json",
        "coinglassSecret": "748094575bdf44cb8dbee2a23a6b80af"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        json_data = response.json()
        if json_data.get("success") and "data" in json_data:
            return json_data["data"].get("BTCUSDT", [])
        else:
            return []
    except Exception as e:
        print("API Hatası:", e)
        return []