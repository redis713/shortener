from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .db import SessionLocal, engine
from datetime import datetime
from .redis_client import redis_client

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "ok"}


@app.post("/api/shorten", response_model=schemas.URLResponse)
def shorten_url(data: schemas.URLCreate, db: Session = Depends(get_db)):
    url = crud.create_short_url(db, str(data.original_url))
    return {"short_code": url.short_code}


@app.get("/api/urls", response_model=schemas.URLList)
def list_urls(db: Session = Depends(get_db)):
    urls = crud.get_all_urls(db)

    result = []

    for url in urls:
        redis_clicks = redis_client.get(f"clicks:{url.short_code}")
        total_clicks = url.clicks + int(redis_clicks or 0)

        result.append({
            "original_url": url.original_url,
            "short_code": url.short_code,
            "clicks": total_clicks,
            "created_at": url.created_at,
            "expires_at": url.expires_at
        })

    return {"urls": result}


@app.get("/api/info/{short_code}", response_model=schemas.URLInfo)
def get_info(short_code: str, db: Session = Depends(get_db)):
    url = crud.get_url(db, short_code)

    if not url:
        raise HTTPException(status_code=404, detail="Not found")

    redis_clicks = redis_client.get(f"clicks:{short_code}")

    total_clicks = url.clicks + int(redis_clicks or 0)

    return {
        "original_url": url.original_url,
        "short_code": url.short_code,
        "clicks": total_clicks,
        "created_at": url.created_at,
        "expires_at": url.expires_at
    }


@app.get("/{short_code}")
def redirect(short_code: str, db: Session = Depends(get_db)):
    cached_url = redis_client.get(short_code)

    if cached_url:
        # увеличиваем счётчик в Redis
        redis_client.incr(f"clicks:{short_code}")
        return RedirectResponse(cached_url)

    url = crud.get_url(db, short_code)

    if not url:
        raise HTTPException(status_code=404, detail="Not found")

    if url.expires_at < datetime.utcnow():
        raise HTTPException(status_code=410, detail="Link expired")

    ttl_seconds = int((url.expires_at - datetime.utcnow()).total_seconds())
    # кладём в кеш
    if ttl_seconds > 0:
        redis_client.setex(short_code, ttl_seconds, url.original_url)

    # увеличиваем Redis-счётчик
    redis_client.incr(f"clicks:{short_code}")

    return RedirectResponse(url.original_url)
