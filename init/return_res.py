from bson import json_util
from django.http import HttpResponse


def http_response(data, code=200, msg=''):
    '''
     返回的数据
     msg 如果为空 会根据code 来确定msg
    '''
    msg = msg if msg else '操作成功' if code == 200 else '操作失败'
    return HttpResponse(json_util.dumps({'code': code, 'msg': msg, 'data': data or {}}, ensure_ascii=False))
