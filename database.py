from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm.session import sessionmaker

from generate_short_url import generate_url
from init_db import Urls, engine


def create_url(original_url: str):
    Session = sessionmaker(bind=engine)

    with Session() as session:
        try:
            short_url = generate_url(4)
            url = Urls(original_url=original_url, short_url=short_url)
            session.add(url)
            session.commit()

            return short_url

        except IntegrityError as e:
            session.rollback()
            return f"IntegrityError: {e}"
        except SQLAlchemyError as e:
            session.rollback()
            return f"Database error: {e}"


def get_url(short_url: str):
    Session = sessionmaker(bind=engine)
    try:
        with Session() as session:
            query = select(Urls.original_url, Urls.expires_at).where(
                Urls.short_url == short_url
            )
            url = session.execute(query).first()
    except IntegrityError as e:
        return f"IntegrityError: {e}"
    except SQLAlchemyError as e:
        return f"Database error: {e}"

    if url is not None:
        return url
    return None


def get_urls():
    Session = sessionmaker(bind=engine)
    try:
        with Session() as session:
            query = select(Urls).where()
            urls = session.scalars(query).all()
    except IntegrityError as e:
        return f"IntegrityError: {e}"
    except SQLAlchemyError as e:
        return f"Database error: {e}"

    if urls is not None:
        return urls
    return None


def update_clicks(short_url: str, clicks: int):
    Session = sessionmaker(bind=engine)

    with Session() as session:
        try:
            select_clicks = select(Urls.clicks).where(Urls.short_url == short_url)
            result_click = session.scalars(select_clicks).first()
            if result_click is None:
                return None

            query = (
                update(Urls)
                .where(Urls.short_url == short_url)
                .values(clicks=(clicks + result_click))
            )

            session.execute(query)
            session.commit()

        except IntegrityError as e:
            session.rollback()
            return f"IntegrityError: {e}"
        except SQLAlchemyError as e:
            session.rollback()
            return f"Database error: {e}"
