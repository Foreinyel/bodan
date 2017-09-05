from . import Base
from sqlalchemy import Column, String, Integer, DateTime,Numeric
import datetime

class Match500History(Base):
    __tablename__ = 'match_500_history'
    id = Column(Integer, primary_key=True)
    match_id = Column(Integer)
    league_name = Column(String(45))
    start_date = Column(DateTime)
    history_url = Column(String(45))
    home = Column(String(45))
    away = Column(String(45))
    home_goal = Column(Integer)
    away_goal = Column(Integer)
    create_time = Column(DateTime, nullable=False)
    update_time = Column(DateTime, nullable=False)

    def __init__(self):
        self.create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.update_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")