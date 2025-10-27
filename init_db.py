import os
from datetime import datetime, timezone, timedelta

from dotenv import load_dotenv
from sqlalchemy import Column, DateTime, Integer, String, create_engine, Boolean
from sqlalchemy.orm import declarative_base

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, echo=True)

Base = declarative_base()


class Urls(Base):
    __tablename__ = "urls"
    id = Column(Integer, primary_key=True, index=True)
    short_url = Column(String(6), unique=True, nullable=False)
    original_url = Column(String(2048), nullable=False)
    clicks = Column(Integer, default=0)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    expires_at = Column(DateTime, default=lambda: datetime.now(timezone.utc) + timedelta(days=7))


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully.")
