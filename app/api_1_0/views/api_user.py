# -*- coding: utf-8 -*-
'''
    用户逻辑操作类
'''
from hashlib import md5
import time

from flask import abort, g, current_app
from flask_restful import (
    Resource,
    reqparse,  # 数据验证
    marshal_with,  # 认证模板的装饰器
    fields
)
from app.models.user import User
from app.models import db_session
from . import auth


class UserAPI(Resource):
    """用户api"""

    def __init__(self):
        # 参数验证
        self.reqparse = reqparse.RequestParser()
        # 添加需要验证的数据
        self.reqparse.add_argument(
            'phone_number',
            type=str,
            help='请提供手机号码',
            required=True
        )
        self.reqparse.add_argument(
            'username',
            type=str,
            help='为自己去一个昵称吧'
        )
        self.reqparse.add_argument(
            'password',
            type=str,
            help='密码不允许为空',
            required=True
        )

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            'token',
            type=str,
            help='请提供手机号码',
            required=True,
            location='headers'
        )

        token = parser.parse_args().get('token').strip()

        phone_number = current_app.redis.get('token:{}'.format(token))
        username = current_app.redis.hget('user:{}'.format(phone_number), 'username')

        if username:
            return {'message': '该{}号码的用户是{}'.format(phone_number, username.decode('utf-8'))}, 200
        return {'message': '该{}号码还未被使用'.format(phone_number.decode('utf-8'))}, 400

    @auth.get_password
    def post(self):
        '''
            用户注册
        '''
        phone_number, username, password = self.reqparse.parse_args().values()
        phone_number = int(phone_number.strip())
        password
        # 查询用户是否已经注册过
        user_exists = User.query.filter_by(phone_number=phone_number).first()
        if user_exists:
            return self.login(user_exists, password)
        else:
            user = User()
            user.hash_password = password
            user.username = username
            # 电话号码
            user.phone_number = phone_number
            db_session.add(user)

            try:
                db_session.commit()
            except Exception as e:
                print(e)
                db_session.rollback()
                return {'message': '注册失败'}, 400
            sc = self.login(user, password)
        return {'message': '欢迎{}用户加入'.format(user.username), 'token': sc[0]['token']}, 200

    def login(self, user_exists, password):
        '''
            用户登录
        '''
        # 创建一个新用户用密码验证测试
        user = User()
        user.hash_password = password

        if user.password_hash != user_exists.password_hash:
            return {'message': '密码不正确'}, 400
        m = md5()

        m.update(user_exists.phone_number.encode('utf-8'))
        m.update(user.hash_password.encode('utf-8'))
        m.update(str(int(time.time())).encode('utf-8'))
        token = m.hexdigest()

        # 创建redis通道
        pipeline = current_app.redis.pipeline()
        # 存入当前该用户的状态与信息
        pipeline.hmset(
            'user:{0}'.format(user_exists.phone_number), {
                'token': token,
                'username': user_exists.username,
                'app_online': 1}  # 是否在线登录
        )
        pipeline.set('token:{}'.format(token), user_exists.phone_number)
        pipeline.expire('user:{0}'.format(
            user_exists.phone_number), 3600 * 24 * 7)
        # 关闭通道
        pipeline.execute()

        return {'token': token, 'message': '欢迎回来{0}'.format(user_exists.username)}, 200
# http://www.bjhee.com/flask-ext6.html
