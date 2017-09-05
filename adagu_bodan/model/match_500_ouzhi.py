from . import Base
from sqlalchemy import Column, String, Integer, DateTime,Numeric,ForeignKey
import datetime

class Match500Ouzhi(Base):
    __tablename__ = 'match_500_ouzhi'
    id = Column(Integer, primary_key=True)
    match_id = Column(Integer,ForeignKey("match_500.id"))
    comp = Column(String(45))
    returns = Column(String(45))
    win = Column(Numeric)
    draw = Column(Numeric)
    lose = Column(Numeric)
    kelly_win = Column(Numeric)
    kelly_draw = Column(Numeric)
    kelly_lose = Column(Numeric)
    create_time = Column(DateTime, nullable=False)
    update_time = Column(DateTime, nullable=False)

    def __init__(self):
        self.create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.update_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")