from datetime import datetime

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse, RedirectResponse

from database import create_url, get_url, get_urls, update_clicks, delete_expired_urls

app = FastAPI()


@app.post("/shorten")
def create(url: str):
    if not url:
        raise HTTPException(status_code=400, detail="Parameter URL not sent.")

    result = create_url(url)

    if isinstance(result, Exception):
        raise HTTPException(
            status_code=500,
            detail="There was an error with the database, please try again later.",
        )
    return JSONResponse({"short-url": result}, 201)


@app.get("/get/{short_url}")
def access(short_url: str):
    url = get_url(short_url)

    if url is not None:
        if isinstance(url, Exception):
            raise HTTPException(
                status_code=500,
                detail="There was an error with the database, please try again later.",
            )

        date = datetime.now()
        original_url = url[0]
        expires_at = datetime.strptime(str(url[1]), "%Y-%m-%d %H:%M:%S")

        if date < expires_at:
            update_clicks(short_url, 1)
            return RedirectResponse(str(original_url), 302)

    delete_expired_urls(short_url)
    return JSONResponse({"error": "Url not found."}, 404)


@app.get("/urls")
def urls():
    urls = get_urls()

    if urls is not None:
        if isinstance(urls, Exception):
            raise HTTPException(
                status_code=500,
                detail="There was an error with the database, please try again later.",
            )

        json_urls = jsonable_encoder(urls)
        return JSONResponse({"urls": json_urls}, 200)
    return JSONResponse({"error": "URLs not found."}, 404)
