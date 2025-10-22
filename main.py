from fastapi import FastAPI
from fastapi.exceptions import HTTPException

from database import create_url

app = FastAPI()


@app.post("/shorten")
def create(url: str):
    if not url:
        raise HTTPException(status_code=400, detail="Parameter URL not sent.")

    result = create_url(url)

    if "error" in result.lower():
        raise HTTPException(status_code=500, detail=result)
    return {"short-url": result}
