from fastapi import FastAPI, Query
from app.kcsc_client import get_codeviewer

app = FastAPI()

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/kcsc/codeviewer/section/{Type}/{Code}")
async def kcsc_codeviewer_section(
    Type: str,
    Code: str,
    title: str = Query(...)
):
    data = await get_codeviewer(Type, Code)

    doc = data[0]
    filtered = []

    for item in doc.get("list", []):
        if title in item.get("title", ""):
            filtered.append({
                "title": item.get("title"),
                "contents": item.get("contents")
            })

    return {
        "code": doc.get("code"),
        "name": doc.get("name"),
        "version": doc.get("version"),
        "section": filtered
    }
