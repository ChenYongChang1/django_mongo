from django.shortcuts import render
from django.http import response, request, HttpResponse
import json
from config.error_config import BAD_PARAMS
from util.auth import use_token_get_data
from server.query import QueryObj
from init.return_res import http_response
from util.check_method import checkMethodGET, checkMethodPOST


# Create your views here.

def demo(request):
    return HttpResponse('hello query')


@checkMethodGET
def dbs(request):
    token = request.META.get('HTTP_ASSTOKEN')
    query = QueryObj('dbs').getDbs(token)
    return http_response(query['data'], query['code'], query['msg'])


# 查询表
@checkMethodGET
def query_table(request):
    token = request.META.get('HTTP_ASSTOKEN')
    db = request.GET.get('db')
    if not db:
        raise Exception(BAD_PARAMS)
    query = QueryObj(db).getTable(token, db)
    return http_response(query['data'], query['code'], query['msg'])


@checkMethodPOST
def query_data(request):
    token = request.META.get('HTTP_ASSTOKEN')
    try:
        data = json.loads(request.body)
    except Exception:
        raise Exception(BAD_PARAMS)
    db = data.get('db')
    table = data.get('table')
    # remove = data.get('remove')
    data['token'] = token
    query = QueryObj(db, table).get_data(data)
    # if remove and len(remove) or table == 'user' and query['data'] and query['data'].get('list'):
    #     post_data = list(query['data']['list']).copy()
    #     remove = remove or []
    #     remove.append('password')
    #     for i in post_data:
    #         for row in i:
    #             if row in remove:
    #                 i[row] = ''
    #         # if 'password' in i:
    #         #     i['password'] = ''
    #     else:
    #         query['data']['list'] = post_data.copy()
    return http_response(query['data'], query['code'], query['msg'])
