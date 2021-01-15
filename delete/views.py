from django.http import response, request, HttpResponse
import json
from bson import json_util

from config.error_config import BAD_PARAMS
from server.delete import DeleObj
from util.check_method import checkMethodPOST
from init.return_res import http_response


@checkMethodPOST
def delete_data(request):
    token = request.META.get('HTTP_ASSTOKEN')
    try:
        data = json.loads(request.body)
    except Exception:
        raise Exception(BAD_PARAMS)
    db = data.get('db')
    table = data.get('table')
    data['token'] = token
    data['path'] = request.path
    delete = DeleObj(db, table).deleData(data)
    return http_response(delete['data'], delete['code'], delete['msg'])


@checkMethodPOST
def drop(request):
    token = request.META.get('HTTP_ASSTOKEN')
    try:
        data = json.loads(request.body)
    except Exception:
        raise Exception(BAD_PARAMS)
    db = data.get('db')
    table = data.get('table')
    data['token'] = token
    data['path'] = request.path
    delete = DeleObj(db, table).dropData(data)
    return http_response(delete['data'], delete['code'], delete['msg'])
