from . import Base
from sqlalchemy import Column, String, Integer, DateTime,Numeric,ForeignKey
import datetime

class Match500Bifen(Base):
    __tablename__ = "match_500_bifen"
    id=Column(Integer,primary_key=True)
    match_id=Column(Integer,ForeignKey("match_500.id"))
    comp = Column(String(45))
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
    create_time = Column(DateTime, nullable=False)
    update_time = Column(DateTime, nullable=False)

    def __init__(self):
        self.create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.update_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")