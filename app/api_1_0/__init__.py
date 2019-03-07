# -*- coding: utf-8 -*-
'''
    v1主程序使用蓝图
'''
from flask import Blueprint
api1_page = Blueprint('api1_page', __name__)

from . import routes
