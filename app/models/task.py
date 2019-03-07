# -*- coding: utf-8 -*-
'''
    任务模型
'''
import datetime

from sqlalchemy import (
    ForeignKey, Column, Integer, Float, Boolean,
    String, Text, DateTime,
)
from . import Conf, Base


class Tasks(Base):
    '''
        任务类
    '''
    __tablename__ = 'tasks'
    id = Column('id', Integer, primary_key=True)
    title = Column('title', String(100), index=True)
    description = Column('description', String(900))
    done = Column('done', Boolean, index=True, default=False)
    register_time = Column('register_time', DateTime,
                           index=True, default=datetime.datetime.now)
