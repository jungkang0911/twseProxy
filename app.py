from fastapi import FastAPI, Query
import httpx, random, asyncio, urllib3

# 關閉 SSL 警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = FastAPI()

# 若要使用代理，可在這裡放入代理網址清單
# 範例: ["http://user:pass@proxy1:8000"]
PROXIES = [None]

# 建立可重試的請求
async def fetch_with_retry(url, params, proxy=None, retries=3):
    for attempt in range(retries):
        try:
            # 若有指定 proxy，用 ProxyTransport
            if proxy:
                transport = httpx.ProxyTransport(proxy_url=proxy)
                async with httpx.AsyncClient(verify=False, transport=transport, timeout=20) as client:
                    r = await client.get(url, params=params)
            else:
                async with httpx.AsyncClient(verify=False, timeout=20) as client:
                    r = await client.get(url, params=params)

            return {"status": r.status_code, "data": r.json()}

        except Exception as e:
            # 若失敗則退避重試
            if attempt < retries - 1:
                await asyncio.sleep(2 ** attempt + random.random())
            else:
                return {"error": str(e)}

@app.get("/fetch")
async def fetch_data(stock_code: str = Query(...), date: str = Query(...)):
    """
    代理抓取台灣證交所 API
    範例：
      /fetch?stock_code=2330&date=20251001
    """
    url = "https://www.twse.com.tw/rwd/zh/afterTrading/STOCK_DAY"
    params = {"date": date, "stockNo": stock_code, "response": "json"}
    proxy = random.choice(PROXIES)
    return await fetch_with_retry(url, params, proxy)
