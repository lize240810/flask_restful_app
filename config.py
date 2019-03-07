# -*- coding: utf-8 -*-
'''
    公共配置文件
'''

class Config(object):
    # flask 密匙
    SECRET_KEY = '123456'


class DevelopmentConfig(Config):
    '''
        开发阶段配置
    '''
    DEBUG = True
    HOST = '127.0.0.1'
    PORT = '5002'

    # redis 数据库
    REDIS_HOST = 'localhost'
    REDIS_PORT = '6379'
    REDIS_DB = 2
    REDIS_PASSWORD = ''
    # sqlalchemy 引擎
    MYSQL_INFO = 'mysql+pymysql://root:root@127.0.0.1:3306/test1?charset=utf8'
    

class ProductionConfig(Config):
    '''
        运行阶段配置
    '''
    DEBUG = False
    HOST = '0.0.0.0'
    PORT = '5002'

    # redis 数据库
    REDIS_HOST = 'server_ip'
    REDIS_PORT = '6379'
    REDIS_DB = 2
    REDIS_PASSWORD = ''
    MYSQL_INFO = 'mysql+pymysql://****:pass@server_ip:3306/test?charset=utf-8'

Conf = DevelopmentConfig

