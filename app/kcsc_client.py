import os
import httpx

KCSC_API_KEY = os.getenv("KCSC_API_KEY")
BASE_URL = "https://kcsc.re.kr"

async def get_codeviewer(doc_type: str, code: str):
    if not KCSC_API_KEY:
        return {"error": "KCSC_API_KEY not set"}

    url = f"{BASE_URL}/OpenApi/CodeViewer/{doc_type}/{code}"
    params = {"key": KCSC_API_KEY}

    async with httpx.AsyncClient(timeout=20) as client:
        r = await client.get(url, params=params)
        r.raise_for_status()
        return r.json()

