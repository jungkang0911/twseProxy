from fastapi import FastAPI, Query
import requests, random

app = FastAPI()

# 若你未設定代理，Render 會用自己的 IP 對外發請求
PROXIES = [None]

@app.get("/fetch")
def fetch_data(stock_code: str, date: str):
    """
    代理抓取台灣證交所 API
    範例:
    /fetch?stock_code=2330&date=20251001
    """
    url = "https://www.twse.com.tw/rwd/zh/afterTrading/STOCK_DAY"
    params = {"date": date, "stockNo": stock_code, "response": "json"}
    proxy = random.choice(PROXIES)
    try:
        r = requests.get(url, params=params, proxies={"http": proxy, "https": proxy}, timeout=20)
        return {"status": r.status_code, "data": r.json()}
    except Exception as e:
        return {"error": str(e)}
