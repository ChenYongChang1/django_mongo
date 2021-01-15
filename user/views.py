import json

from django.shortcuts import render
from server.user import Login
from config.error_config import LOGIN_ERROR
from init.return_res import http_response
from util.check_method import checkMethodPOST,checkMethodGET
# Create your views here.

@checkMethodPOST
def login(request):
    user_message = json.loads(request.body)
    login_server = Login()
    try:
        login_data = login_server.login(user_message)
    except Exception as e:
        print(e)
        return http_response({}, LOGIN_ERROR)
    print(login_data, 'login_data')
    code, msg, data = login_data.values()
    return http_response(data, code, msg)
