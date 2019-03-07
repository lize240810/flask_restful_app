# -*- coding: utf-8 -*-
'''
	路由层
'''
from flask_restful import Api
# 导入视图模块
# import ipdb; ipdb.set_trace()
from .views.api_task import Helloword, TaskListAPI, TaskAPI
from .views.api_user import UserAPI
# 导入蓝图路由
from . import api1_page
# 实例化路由
api = Api(api1_page)

# 注册路由
# api.add_resource(Servers, '/servers')
# api.add_resource(Server, '/servers/<_id>')

# # 注册路由
api.add_resource(Helloword, '/', endpoint='home')
# # 检索全部任务的路由
api.add_resource(TaskListAPI, '/api/v1.0/tasks', endpoint='tasks')

# # 查询单个任务 更删除 修改
api.add_resource(TaskAPI, '/api/v1.0/task/<int:id>', endpoint='task')
api.add_resource(UserAPI, '/api/v1.0/user', endpoint='user')

# # http://127.0.0.1:5000/api/v1.0/task/33 请求uri