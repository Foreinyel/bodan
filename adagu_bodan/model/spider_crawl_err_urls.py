from . import Base
from sqlalchemy import Column, String, Integer, DateTime,Numeric,BLOB
import datetime

class SpiderCrawlErrUrls(Base):
    __tablename__ = 'spider_crawl_err_urls'
    id = Column(Integer, primary_key=True)
    spider_name = Column(String(200))
    req_url = Column(String(200))
    txt = Column(BLOB)
    create_time = Column(DateTime, nullable=False)
    update_time = Column(DateTime, nullable=False)

    def __init__(self):
        self.create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.update_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")