from . import Base
from sqlalchemy import Column, String, Integer, DateTime,Numeric
import datetime

class Match500(Base):
    __tablename__ = 'match_500'
    id = Column(Integer, primary_key=True)
    round_txt = Column(String(45))
    start_time = Column(DateTime)
    home_txt = Column(String(200))
    away_txt = Column(String(200))
    home = Column(String(45))
    away = Column(String(45))
    home_short = Column(String(45))
    away_short = Column(String(45))
    home_goal = Column(Integer)
    away_goal = Column(Integer)
    home_standing_before = Column(Integer)
    away_standing_before = Column(Integer)
    create_time = Column(DateTime, nullable=False)
    update_time = Column(DateTime, nullable=False)
    predict_win_no_win=Column(Integer)
    ouzhi_odds_aomen=Column(Numeric)
    profit=Column(Numeric)

    def __init__(self):
        self.create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.update_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")