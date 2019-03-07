# -*- coding:utf-8 -*-
'''
    模型启动类
'''

from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, backref, sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from config import Conf

# 创建引擎
engine = create_engine(Conf.MYSQL_INFO, echo=True)  # echo = True 是否打印sql语句
# 声明基础
Base = declarative_base()

# 创建会话作用域
db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)

# 创建代理查询
Base.query = db_session.query_property()



from . import task, user
