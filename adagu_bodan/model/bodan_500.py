from . import Base
from sqlalchemy import Column, String, Integer, DateTime,Numeric
import datetime

class Bodan500(Base):
    __tablename__ = "bodan_500"
    id=Column(Integer,primary_key=True)
    league=Column(String(45))
    start_time=Column(DateTime)
    home=Column(String(45))
    away=Column(String(45))
    home_goal=Column(Integer)
    away_goal=Column(Integer)
    odds_comp=Column(String(45))
    one_zero=Column(String(45))
    two_zero=Column(String(45))
    two_one=Column(String(45))
    three_zero=Column(String(45))
    three_one=Column(String(45))
    three_two=Column(String(45))
    four_zero=Column(String(45))
    four_one=Column(String(45))
    four_two=Column(String(45))
    four_three=Column(String(45))
    zero_one =Column(String(45))
    zero_two =Column(String(45))
    one_two=Column(String(45))
    zero_three=Column(String(45))
    one_three=Column(String(45))
    two_three=Column(String(45))
    zero_four=Column(String(45))
    one_four=Column(String(45))
    two_four=Column(String(45))
    three_four=Column(String(45))
    zero_zero=Column(String(45))
    one_one=Column(String(45))
    two_two=Column(String(45))
    three_three=Column(String(45))
    four_four=Column(String(45))
    returns=Column(String(45))
    create_time = Column(DateTime, nullable=False)
    update_time = Column(DateTime, nullable=False)
    hit_standing = Column(Integer)
    lowest_odds = Column(Numeric)
    hit_odds = Column(Numeric)
    profit = Column(Numeric)
    win_or_lose = Column(Integer)
    win_no_win=Column(Integer)
    predict_win_no_win=Column(Integer)
    win_no_win_profit=Column(Numeric)
    win_no_win_cost=Column(Numeric)

    def __init__(self):
        self.create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.update_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")