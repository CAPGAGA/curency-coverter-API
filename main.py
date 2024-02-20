from typing import Union, List
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from starlette import status
import logging
import models
import schemas
from database import engine, get_db

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.on_event('startup')
async def startup():
    logger.log(logging.INFO, msg='starting up api')
    logger.log(logging.INFO, msg='creating db ')
    models.Base.metadata.create_all(bind=engine)

@app.get('/')
async def read_root():

    return {'Hello': 'World'}