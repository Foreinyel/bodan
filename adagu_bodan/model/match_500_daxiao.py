from . import Base
from sqlalchemy import Column, String, Integer, DateTime,Numeric
import datetime

class Match500Daxiao(Base):
    __tablename__ = 'match_500_daxiao'
    id = Column(Integer, primary_key=True)
    match_id = Column(Integer)
    comp = Column(String(45))
    handicap = Column(String(45))
    over = Column(Numeric)
    under = Column(Numeric)
    create_time = Column(DateTime, nullable=False)
    update_time = Column(DateTime, nullable=False)

    def __init__(self):
        self.create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.update_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")