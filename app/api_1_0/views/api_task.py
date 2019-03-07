# -*- coding: utf-8 -*-
'''
	主程序
'''
from flask import abort, url_for
from flask_restful import (
    Resource,
    reqparse,  # 验证数据
    marshal,  # 把id转化成uri并且能够转换其他的参数
    fields  # 字段
)

from app.models.task import Tasks
from app.models import db_session
from . import auth

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]

# 作为marshal认证的模板
task_fields = {
    'title': fields.String,
    'description': fields.String,
    'done': fields.Boolean,
    # 'uri': fields.Url('task', absolute=True, scheme='https'),
}


class Helloword(Resource):
    '''方法 可以使用get和put两种方式访问'''

    def get(self):
        # 直接查询字典
        return {'hello': 'hello world'}


class TaskListAPI(Resource):

    def __init__(self):
        # Flask-RESTful 提供了一个更好的方式来处理数据验证，它叫做 RequestParser 类
        self.reqparse = reqparse.RequestParser()
        # 数据验证
        self.reqparse.add_argument(
            'title',
            type=str,
            required=True,
            help='未提供任务标题'
        )

        self.reqparse.add_argument(
            'description',
            type=str,
            default="",
            location='json'
        )

    def get(self):
        '''
            检索任务列表
        '''
        
        return {'result': '查询全部'}

    @auth.login_required
    def post(self):
        '''
            创建新任务
        '''
        title, description = self.reqparse.parse_args()
        title = title.strip()
        description = description.strip()

        task = tasks(title, description)
        db_session.add(task)

        try:
            db_session.commit()
        except Exception as e:
            print(e)
            db_session.rollback()

        return {'message': '成功添加任务'}, 200


class TaskAPI(Resource):
    '''
        检索某个任务列表
    '''

    def __init__(self):
        # Flask-RESTful 提供了一个更好的方式来处理数据验证，它叫做 RequestParser 类
        self.parser = reqparse.RequestParser()
        # self.reqparse = reqparse.RequestParser()
        # 数据验证
        self.parser.add_argument(
            'title',
            type=str,
            required=True,  # 必须的参数
            help='未提供任务标题',
            # action='append', 多个值盒列表
            # location='json', # 参数位置
            # location='args'
            # dest='public_name' 存储为不同的名称
        )

        self.parser.add_argument(
            'description',
            type=str,
            # location='json'
        )

        self.parser.add_argument(
            'done',
            type=bool,
            # location='json'
        )

    def get(self, id):
        return {'result': '这是第{0}个任务'.format(id)}

    def put(self, id):
        '''
            更新任务
        '''

        # 从总数据中查询
        for i in tasks:
            if i['id'] == id:
                task = i
        # 判断是否为空
        if len(task) == 0:
            abort(404)
        # 使用了请求解析 必须传入三个参数

        for k, v in self.parser.parse_args().items():

            if v != None:
                if type(v) == str:
                    task[k] = v.strip()
                else:
                    task[k] = v

        # marshal实际上是您的数据对象并应用字段过滤。编组可以处理单个对象，dicts或对象列表。
        return {'task': marshal(task, task_fields)}, 201

    def delete(self, id):
        '''
            删除任务
        '''
        return {'result': '删除第{0}个任务'.format(id)}
