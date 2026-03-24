from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from . import models
from .utils import generate_short_code
from .config import settings

def create_short_url(db: Session, original_url: str):
    short_code = generate_short_code()
    expires_at = datetime.utcnow() + timedelta(days=settings.LINK_TTL_DAYS)

    db_url = models.URL(
        original_url=original_url,
        short_code=short_code,
        expires_at=expires_at
    )

    db.add(db_url)
    db.commit()
    db.refresh(db_url)

    return db_url


def get_url(db: Session, short_code: str):
    return db.query(models.URL).filter(models.URL.short_code == short_code).first()

def get_all_urls(db: Session):
    return db.query(models.URL).all()
