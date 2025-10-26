from fastapi import FastAPI, Query
import requests, random, urllib3

# 關閉 SSL 驗證警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = FastAPI()

# 代理清單（可加上自己的代理 IP）
PROXIES = [None]  # 範例: ["http://user:pass@proxy1:8000", "http://proxy2:8080"]

@app.get("/fetch")
def fetch_data(stock_code: str = Query(...), date: str = Query(...)):
    """
    代理抓取台灣證交所 API
    範例：
      /fetch?stock_code=2330&date=20251001
    """
    url = "https://www.twse.com.tw/rwd/zh/afterTrading/STOCK_DAY"
    params = {"date": date, "stockNo": stock_code, "response": "json"}
    proxy = random.choice(PROXIES)

    try:
        # 加上 verify=False 修正 SSL 憑證錯誤
        r = requests.get(
            url,
            params=params,
            proxies={"http": proxy, "https": proxy},
            timeout=20,
            verify=False
        )

        return {"status": r.status_code, "data": r.json()}
    except requests.RequestException as e:
        return {"error": str(e)}
