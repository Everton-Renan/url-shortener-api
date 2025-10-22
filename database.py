from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm.session import sessionmaker

from generate_short_url import generate_url
from init_db import Urls, engine


def create_url(original_url: str):
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        short_url = generate_url(4)
        url = Urls(original_url=original_url, short_url=short_url)
        session.add(url)
        session.commit()
    except IntegrityError as e:
        session.rollback()
        return f"IntegrityError: {e}"
    except SQLAlchemyError as e:
        session.rollback()
        return f"Database error: {e}"
    finally:
        session.close()

    return short_url


def get_url(short_url: str):
    Session = sessionmaker(bind=engine)
    session = Session()

    query = select(Urls).where(Urls.short_url == short_url)
    url = session.scalars(query).first()
    if url is not None:
        return url.original_url
    return None
