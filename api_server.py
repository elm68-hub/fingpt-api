from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import os

app = FastAPI()

class Message(BaseModel):
    role: str
    content: str

class AnalysisRequest(BaseModel):
    messages: List[Message]
    asset: Optional[str] = None
    timeframe: Optional[str] = None

class AnalysisResponse(BaseModel):
    content: str
    sources: List[str]
    confidence: Optional[float] = None

@app.post("/analyze")
async def analyze(request: AnalysisRequest):
    try:
        user_message = next((m.content for m in request.messages if m.role == "user"), "")

        response_content = f"""## Analyse FinGPT

**Actif analysé:** {request.asset or "Général"}

**Question:** {user_message}

### Analyse
Cette analyse sera générée par FinGPT une fois le modèle chargé.

*Service FinGPT opérationnel*
"""

        return AnalysisResponse(
            content=response_content,
            sources=["FinGPT v3.3"],
            confidence=0.85
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    return {"status": "ok", "model": "FinGPT"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
