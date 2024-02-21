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
    seed_db()

@app.post('/convert/{from}/{to}/{amount}')
async def read_root(from_cur:str, to_cur:str, amount:float, db: Session = Depends((get_db))):

    from_cur_data = db.query(models.Currency)\
        .filter(models.Currency.name == from_cur)\
        .order_by(models.Currency.date.desc()).first()

    to_cur_data = db.query(models.Currency).\
        filter(models.Currency.name == to_cur).\
        order_by(models.Currency.date.desc()).first()

    if not from_cur_data or not to_cur_data:
        return HTTPException(status_code=404, detail='Conversion rates for this pair is not available')

    return round(Decimal(str(amount)) * 1/from_cur_data.rate * to_cur_data.rate, 2)
