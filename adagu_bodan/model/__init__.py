# -*- coding: utf-8 -*-
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine,Column,String,Integer,DateTime
from sqlalchemy.orm import sessionmaker
from scrapy.utils.project import get_project_settings

# 创建对象的基类:
Base = declarative_base()

# 获取项目配置
settings = get_project_settings()
db_uri = settings["MYSQL_DATABASE_URI"]

# 初始化数据库连接:
engine = create_engine(db_uri, encoding="utf-8", echo=True,pool_size=20, max_overflow=0)

#返回数据库会话
def loadSession():
    Session = sessionmaker(bind=engine)
    session = Session()
    return session