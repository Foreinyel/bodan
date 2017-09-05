from . import Base
from sqlalchemy import Column, String, Integer, DateTime,Numeric
import datetime

class Match500Recent(Base):
    __tablename__ = 'match_500_recent'
    id = Column(Integer, primary_key=True)
    match_id = Column(Integer)
    team_type = Column(String(45))
    recent_type = Column(String(45))
    league_name = Column(String(45))
    start_date = Column(DateTime)
    recent_url = Column(String(45))
    home = Column(String(45))
    away = Column(String(45))
    home_goal = Column(Integer)
    away_goal = Column(Integer)
    create_time = Column(DateTime, nullable=False)
    update_time = Column(DateTime, nullable=False)

    def __init__(self):
        self.create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.update_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")