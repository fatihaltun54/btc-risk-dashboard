# data_fetcher.py
import requests
import pandas as pd
from datetime import datetime

API_KEY = "748094575bdf44cb8dbee2a23a6b80af"
HEADERS = {"coinglassSecret": API_KEY}

def fetch_metrics():
    try:
        url = "https://open-api.coinglass.com/public/v2/futures/longShortChart?symbol=BTC"
        r = requests.get(url, headers=HEADERS)
        ls_data = r.json().get("data", {}).get("list", [])[-10:]

        url2 = "https://open-api.coinglass.com/public/v2/fundingRate?symbol=BTC"
        r2 = requests.get(url2, headers=HEADERS)
        f_data = r2.json().get("data", {}).get("BTC", {}).get("list", [])[-10:]

        data = []
        for i in range(min(len(ls_data), len(f_data))):
            timestamp = datetime.utcfromtimestamp(ls_data[i]['time'] / 1000)
            price = ls_data[i]['price']
            long_ratio = ls_data[i]['longAccount']
            short_ratio = ls_data[i]['shortAccount']
            funding_rate = float(f_data[i]['fundingRate'])
            oi = ls_data[i]['value']

            data.append({
                "timestamp": timestamp,
                "price": price,
                "long_ratio": long_ratio,
                "short_ratio": short_ratio,
                "fundingRate": funding_rate,
                "oi": oi
            })

        return pd.DataFrame(data)
    except:
        return pd.DataFrame()
