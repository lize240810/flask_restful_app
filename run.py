# -*-coding: utf-8 -*-
'''
    管理和启动 flask程序
'''
from flask import Flask
from flask_restful import Resource, Api
import redis


# 导入蓝图实例
from app.api_1_0 import api1_page
# 数据库创建
from app.models import *
from config import Conf


def create_app():
    app = Flask(__name__)
    app.config.from_object(Conf)
    # app 密钥
    app.secret_key = app.config['SECRET_KEY']
    # redis 数据库
    app.redis = redis.Redis(
        host=app.config['REDIS_HOST'],
        port=app.config['REDIS_PORT'],
        db=app.config['REDIS_DB'],
        password=app.config['REDIS_PASSWORD']
    )

    # 注册蓝图
    app.register_blueprint(api1_page)
    # 创建数据库
    Base.metadata.create_all(engine)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=Conf.DEBUG)
    