from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm.session import sessionmaker

from generate_short_url import generate_url
from init_db import Urls, engine


def create_url(original: str):
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        short_url = generate_url(4)
        url = Urls(original=original, short_url=short_url)
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
