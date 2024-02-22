import datetime
import logging
logger = logging.getLogger(__name__)

from settings import DB_HOST, DB_PORT, DB_PASSWORD, DB_USERNAME, DB, API_KEY

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

import currencyapicom



db_url = f'postgresql+psycopg2://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB}'

engine = create_engine(db_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# create session for database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# seed database with new conversion rates
def seed_db():
    from models import Currency
    with Session(bind=engine) as session:
        currencies = session.query(Currency).filter(Currency.date == datetime.date.today()).all()
        logger.log(logging.INFO, "checking db for today's rates")
        if not currencies:
            logger.log(logging.INFO, "loading today's rates")
            client = currencyapicom.Client(API_KEY)
            results = client.latest()
            to_save = []
            for cur, cur_data in results.get('data').items():
                to_save.append(Currency(name=cur_data.get('code'), rate=cur_data.get('value')))
                session.add_all(to_save)
                session.commit()

        logger.log(logging.INFO, "rates are up to date")


