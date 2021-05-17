# -*- coding:utf8 -*-
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse, JsonResponse
import jwt

from config.error_config import NOT_LOGIN
from config.white_request import PATH

SECRECT_KEY = "cyc"


class MyMiddle(MiddlewareMixin):
    def open_token(self, token):
        data = jwt.decode(token, SECRECT_KEY, audience='webkit', algorithms=['HS256'])
        return data

    def process_request(self, request):
        print('{}请求，参数:{} '.format(request.method, request))
        white = any(list((x in request.path) for x in PATH))
        if white:
            pass
        elif request.path not in PATH:
            token = request.META.get('HTTP_ASSTOKEN')
            if token:
                try:
                    auth = self.open_token(token).get(
                        'message')
                except Exception as e:
                    auth = ''
                if auth:
                    return
            return JsonResponse({'code': NOT_LOGIN, 'msg': '未登录', 'data': {}})

