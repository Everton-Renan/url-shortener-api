import os
from datetime import datetime, timezone

from dotenv import load_dotenv
from sqlalchemy import Column, DateTime, Integer, String, create_engine
from sqlalchemy.orm import declarative_base

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, echo=True)

Base = declarative_base()


class Urls(Base):
    __tablename__ = "urls"
    id = Column(Integer, primary_key=True, index=True)
    short_url = Column(String(5), unique=True, nullable=False)
    original = Column(String(2048), nullable=False)
    clicks = Column(Integer, default=0)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully.")
