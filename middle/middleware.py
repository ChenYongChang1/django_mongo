# 定义中间件类，处理全局异常
from django.http import HttpResponse, JsonResponse
from django.utils.deprecation import MiddlewareMixin
from bson import json_util
from init.return_res import http_response


class ExceptionTestMiddleware(MiddlewareMixin):
    # 如果注册多个process_exception函数，那么函数的执行顺序与注册的顺序相反。(其他中间件函数与注册顺序一致)
    # 中间件函数，用到哪个就写哪个，不需要写所有的中间件函数。
    def process_exception(self, request, exception):
        '''视图函数发生异常时调用'''
        print(request, exception)
        return HttpResponse(http_response({}, int(str(exception)) if str(exception).isdigit() else 500))
