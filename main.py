from datetime import datetime

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from fastapi.responses import RedirectResponse

from database import create_url, get_url, get_urls, update_clicks

app = FastAPI()


@app.post("/shorten")
def create(url: str):
    if not url:
        raise HTTPException(status_code=400, detail="Parameter URL not sent.")

    result = create_url(url)

    if "error" in result.lower():
        raise HTTPException(status_code=500, detail=result)
    return {"short-url": result}


@app.get("/create/{short_url}")
def access(short_url: str):
    url = get_url(short_url)

    if url is not None:
        date = datetime.now()
        original_url = url[0]
        expires_at = datetime.strptime(str(url[1]), "%Y-%m-%d %H:%M:%S.%f")

        if date < expires_at:
            update_clicks(short_url, 1)
            return RedirectResponse(str(original_url))
    return {"error": "Url not found."}


@app.get("/urls")
def urls():
    urls = get_urls()
    if urls is not None:
        json_urls = jsonable_encoder(urls)
        return json_urls
    return {"error": "URLs not found."}
