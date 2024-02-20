from database import Base
from sqlalchemy import Column, Numeric, String, Integer, text, DATE

class Currency(Base):
    __tablename__ = 'currencies'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    rate = Column(Numeric, nullable=False, server_default='0')
    date = Column(DATE, server_default=text('now()'))


