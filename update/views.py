from django.http import response, request, HttpResponse
import json
from bson import json_util

from config.error_config import BAD_PARAMS
from util.check_method import checkMethodPOST
from server.update import updateObj
from init.return_res import http_response


@checkMethodPOST
def update_data(request):
    token = request.META.get('HTTP_ASSTOKEN')
    try:
        data = json.loads(request.body)
    except Exception:
        raise Exception(BAD_PARAMS)
    db = data.get('db')
    table = data.get('table')
    data['token'] = token
    data['path'] = request.path
    update = updateObj(db, table).updataMess(data)
    return http_response(update['data'], update['code'], update['msg'])

