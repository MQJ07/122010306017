from fastapi import FastAPI, HTTPException, Query
import httpx
import asyncio

app = FastAPI()

async def fetch_numbers(url):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=0.5)
            if response.status_code == 200:
                return set(response.json().get("numbers", []))
        except httpx.TimeoutException:
            pass
    return set()

@app.get("/numbers/")
async def get_merged_numbers(urls: list[str] = Query(..., title="List of URLs")):
    tasks = [fetch_numbers(url) for url in urls]
    collected_numbers = await asyncio.gather(*tasks)
    
    merged_numbers = sorted(set().union(*collected_numbers))
    return {"numbers": merged_numbers}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

