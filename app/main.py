from fastapi import FastAPI, Query
from app.kcsc_client import get_codeviewer

app = FastAPI(
    title="KCSC CodeViewer Proxy (Safe Slice Mode)"
)

# ─────────────────────────────
# Health check
# ─────────────────────────────
@app.get("/health")
def health():
    return {"ok": True}


# ─────────────────────────────
# ❌ 전체 문서 직접 반환 (금지용)
#   → 응답 크기 초과 위험
#   → 디버깅 외 사용 금지
# ─────────────────────────────
@app.get("/kcsc/codeviewer/raw/{Type}/{Code}")
async def kcsc_codeviewer_raw(Type: str, Code: str):
    return await get_codeviewer(Type, Code)


# ─────────────────────────────
# ✅ 부분 조항 슬라이싱 (실사용)
# ─────────────────────────────
@app.get("/kcsc/codeviewer/section/{Type}/{Code}")
async def kcsc_codeviewer_section(
    Type: str,
    Code: str,
    title: str = Query(
        ...,
        description="조항 제목에 포함되는 문자열 (예: '1. 일반사항', '적용범위')"
    )
):
    data = await get_codeviewer(Type, Code)

    # CodeViewer 응답은 리스트 형태
    doc = data[0]

    filtered_sections = []

    for item in doc.get("list", []):
        if title in (item.get("title") or ""):
            filtered_sections.append({
                "no": item.get("no"),
                "sort": item.get("sort"),
                "title": item.get("title"),
                "contents": item.get("contents")
            })

    return {
        "codeType": doc.get("codeType"),
        "code": doc.get("code"),
        "name": doc.get("name"),
        "version": doc.get("version"),
        "updateDate": doc.get("updateDate"),
        "section": filtered_sections
    }
