from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from fastapi.responses import RedirectResponse

from database import create_url, get_url

app = FastAPI()


@app.post("/shorten")
def create(url: str):
    if not url:
        raise HTTPException(status_code=400, detail="Parameter URL not sent.")

    result = create_url(url)

    if "error" in result.lower():
        raise HTTPException(status_code=500, detail=result)
    return {"short-url": result}


@app.get("/{short_url}")
def access(short_url: str):
    original_url = get_url(short_url)
    if original_url is not None:
        return RedirectResponse(str(original_url))
    return {"error": "Url not found."}
