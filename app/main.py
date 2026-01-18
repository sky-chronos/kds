from fastapi import FastAPI
from app.kcsc_client import get_codeviewer

app = FastAPI()

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/kcsc/codeviewer/{Type}/{Code}")
async def kcsc_codeviewer(Type: str, Code: str):
    return await get_codeviewer(Type, Code)
