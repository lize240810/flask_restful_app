# -*- coding: utf-8 -*-
'''
    用户模型
'''
import hashlib

from sqlalchemy import (
    Column, Integer, Float, Boolean, String, Text, DateTime
)
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from . import Conf, Base

# 令牌验证
from itsdangerous import TimedSerializer as Serializer


class User(Base):
    '''
    用户类
    '''
    __tablename__ = 'user'
    id = Column('id', Integer, primary_key=True)
    phone_number = Column('phone_number', String(11), index=True)
    username = Column('username', String(30), index=True)
    password_hash = Column(String(128))

    @hybrid_property
    def hash_password(self):
        if not self.password_hash:
            return ''
        return self.password_hash

    @hash_password.setter
    def hash_password(self, password):
        '''
            密码加密
        '''
        sh128 = hashlib.shake_128()
        sh128.update(str(password).encode("utf-8"))
        pwd_content = sh128.hexdigest(128).upper()
        sh128.update(pwd_content.encode('utf-8'))
        pwd_hash = sh128.hexdigest(128).upper()[:128]
        self.password_hash = pwd_hash
