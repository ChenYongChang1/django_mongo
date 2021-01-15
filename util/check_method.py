# -*- coding:utf8 -*-
from functools import wraps
from init.return_res import http_response
from config.error_config import ONLY_GET, ONLY_POST


# 检查请求方式
def checkMethodPOST(a_func):
    @wraps(a_func)
    def wrapTheFunction(*args):
        # print(*args, 'args')
        if args[0].method.upper() == 'POST':
            return a_func(*args)
        else:
            raise Exception(ONLY_POST)
    return wrapTheFunction


def checkMethodGET(a_func):
    @wraps(a_func)
    def wrapTheFunction(*args):
        if args[0].method.upper() == 'GET':
            return a_func(*args)
        else:
            raise Exception(ONLY_GET)
    return wrapTheFunction
