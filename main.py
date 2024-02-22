from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
import logging
import models
import schemas
from database import engine, get_db, seed_db
from datetime import date
from decimal import Decimal

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()


@app.on_event('startup')
async def startup(db: Session = Depends(get_db)):
    logger.log(logging.INFO, msg='starting up api')
    logger.log(logging.INFO, msg='creating db')
    # models.Base.metadata.create_all(bind=engine)
    # check db status
    seed_db()

@app.post('/convert/{from}/{to}/{amount}')
async def read_root(from_cur:str, to_cur:str, amount:float, db: Session = Depends((get_db))):
    '''
    :param from_cur: currency from which user need to convert
    :param to_cur: currency to which user need to convert
    :param amount: amount of currency to convert
    :return: converted amount
    '''
    # get from currency rate
    from_cur_data = db.query(models.Currency)\
        .filter(models.Currency.name == from_cur.strip().upper())\
        .order_by(models.Currency.date.desc()).first()

    # get to currency rate
    to_cur_data = db.query(models.Currency).\
        filter(models.Currency.name == to_cur.strip().upper()).\
        order_by(models.Currency.date.desc()).first()

    if not from_cur_data or not to_cur_data:
        return HTTPException(status_code=404, detail='Conversion rates for this pair is not available')

    # return amount of to currency
    return round(Decimal(str(amount)) * 1/from_cur_data.rate * to_cur_data.rate, 2)
