# -*- coding: utf-8 -*-

from flask import abort, url_for

from flask_restful import (
	Resource, 
	reqparse, # 验证数据
	marshal, # 把id转化成uri并且能够转换其他的参数
	fields # 字段
)

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

# 作为marshal函数的模板，
task_fields = {
	'title': fields.String,
	'description': fields.String,
	'done': fields.Boolean,
	'uri': fields.Url('task')
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
			type = str, 
			required = True, 
			help = '未提供任务标题'
		)

		self.reqparse.add_argument(
			'description', 
			type = str, 
			default = "", 
			location = 'json'
		)

	def get(self):
		'''
			检索任务列表
		'''
		return {'result': '查询全部'}

	def post(self):
		'''
			创建新任务
		'''
		return {'result': '查询全部'}


class TaskAPI(Resource):
	'''
		检索某个任务列表
	'''
	def __init__(self):
		# Flask-RESTful 提供了一个更好的方式来处理数据验证，它叫做 RequestParser 类
		self.reqparse = reqparse.RequestParser()
		# 数据验证
		self.reqparse.add_argument(
			'title', 
			type = str, 
			required = True, 
			help = '未提供任务标题',
			location = 'json'
		)

		self.reqparse.add_argument(
			'description', 
			type = str, 
			location = 'json'
		)

		self.reqparse.add_argument(
			'done', 
			type = bool, 
			location = 'json'
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

		args = self.reqparse.parse_args()
		for k, v in args.iteritems():
			if v != None:
				task[k] = v
		return  {'task': marshal(task, task_fields) }, 201
	
	def delete(self, id):
		'''
			删除任务
		'''
		return {'result': '删除第{0}个任务'.format(id)}
