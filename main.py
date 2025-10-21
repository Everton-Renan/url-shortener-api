from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from generate_short_url import generate_url

app = FastAPI()
urls: dict[str, str] = dict()


@app.post("/shorten")
def create(url: str):
    if url is None or url is False:
        return {"error": "Parameter URL not sent."}

    short_url = generate_url(4)
    urls[short_url] = url
    return {"short-url": short_url}


@app.get("/{short_url}")
def access(short_url: str):
    for k, v in urls.items():
        if k == short_url:
            return RedirectResponse(v)
    return {"error": "Url not found."}
