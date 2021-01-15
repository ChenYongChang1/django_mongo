import json
import random

from django.shortcuts import render

# Create your views here.
from config.error_config import BAD_PARAMS, DONT_MATCH, SUCCESS
from config.spider_config import FROM_RESOURCE_DICT
from server.add import addObj, get_oss, add_other_resourse
from util.check_method import checkMethodPOST
from init.return_res import http_response
from util.check_method import checkMethodGET, checkMethodPOST


@checkMethodPOST
def add_data(request):
    token = request.META.get('HTTP_ASSTOKEN')
    try:
        data = json.loads(request.body)
    except Exception:
        raise Exception(BAD_PARAMS)
    db = data.get('db')
    table = data.get('table')
    data['token'] = token
    add = addObj(db, table).addData(data)
    return http_response(add['data'], add['code'], add['msg'])


def add_count(request):
    pass

# @checkMethodPOST
# def addphoto(request):
#     token = request.META.get('HTTP_ASSTOKEN')
#     try:
#         data = json.loads(request.body)
#     except Exception:
#         raise Exception(BAD_PARAMS)
#     data['token'] = token
#     add = addObj('').addDataPhoto(data)
#     return http_response(add['data'], add['code'], add['msg'])


@checkMethodPOST
def get_sign_oss(request):
    token = request.META.get('HTTP_ASSTOKEN')
    try:
        data = json.loads(request.body)
    except Exception:
        raise Exception(BAD_PARAMS)
    data['token'] = token
    print(data, "data")
    add = get_oss(data)
    return http_response(add['data'], add['code'], add['msg'])


@checkMethodPOST
def add_other_article(request):
    token = request.META.get('HTTP_ASSTOKEN')
    try:
        data = json.loads(request.body)
    except Exception:
        raise Exception(BAD_PARAMS)
    if not data.get('jsonMessage') or not data.get('jsonMessage').get('url'):
        raise Exception(BAD_PARAMS)
    if not data['jsonMessage'].get('resource'):
        for i in FROM_RESOURCE_DICT:
            if i in data.get('jsonMessage').get('url'):
                data['jsonMessage']['resource'] = i
                break
    else:
        if data['jsonMessage'].get('resource') not in data.get('jsonMessage').get('url'):
            raise Exception(DONT_MATCH)
    data['token'] = token
    content, title_html = add_other_resourse(data)
    data['jsonMessage'] = {
        "title": title_html,
        "content": content,
        "from": data.get('jsonMessage').get('resource'),
        "from_url": data.get('jsonMessage').get('url'),
        "id": 'article_{}_{}_{}'.format(random.random(), data.get('jsonMessage').get('resource'), len(content))
    }
    if data.get('save_db') is False:
        return http_response(data['jsonMessage'], SUCCESS, '获取成功')
    db = data.get('db')
    table = data.get('table')
    data['token'] = token
    add = addObj(db, table).addData(data)
    return http_response(add['data'], add['code'], add['msg'])
