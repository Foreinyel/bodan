from . import Base
from sqlalchemy import Column, String, Integer, DateTime,Numeric
import datetime

class Match500TeamStanding(Base):
    __tablename__ = "match_500_team_standing"
    id = Column(Integer, primary_key=True)
    match_id = Column(Integer)
    type = Column(String(45))
    team_type = Column(String(45))
    match_count = Column(Integer)
    win = Column(Integer)
    draw = Column(Integer)
    lose = Column(Integer)
    goals = Column(Integer)
    lost_goals = Column(Integer)
    total_goals = Column(Integer)
    marks = Column(Integer)
    standing = Column(Integer)
    win_rate = Column(Numeric)
    create_time = Column(DateTime)
    update_time = Column(DateTime)

    def __init__(self):
        self.create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.update_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")