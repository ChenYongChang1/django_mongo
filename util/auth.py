import jwt
from functools import wraps
from config.error_config import SUCCESS, NOT_ALLOW, BAD_PARAMS

SECRECT_KEY = 'cyc'


def open_token(token):
    data = jwt.decode(token, SECRECT_KEY, audience='webkit', algorithms=['HS256'])
    return data


def use_token_get_data(token):
    cound_list = open_token(token).get('message').get('cound')
    admin_people = open_token(token).get('message').get('type0')
    super_admin = open_token(token).get('message').get('superAdmin')
    return cound_list, super_admin, admin_people


def check_auth(fuc):
    @wraps(fuc)
    def wrap_the_function(*args):
        try:
            data = args[1]
        except Exception as e:
            print(e)
            data = args[0]
        print('data', data)
        cound_list, super_admin, admin_people = use_token_get_data(data.get('token'))
        if super_admin or admin_people:
            if 'admin_user' != data.get('db') or super_admin:
                return fuc(*args)
            else:
                raise Exception(NOT_ALLOW)
        else:
            if not data.get('db') or data.get('db') in cound_list:
                return fuc(*args)
        raise Exception(NOT_ALLOW)

    return wrap_the_function


# 删除的权限 修改权限
def checkDeleAuth(fuc):
    @wraps(fuc)
    def wrapTheFunction(*args):
        try:
            data = args[1]
            cound_list, super_admin, admin_people = use_token_get_data(data.get('token'))
            print(cound_list, super_admin, admin_people)
            if super_admin or admin_people:
                if super_admin:
                    return fuc(*args)
                elif admin_people:
                    if 'delete' in args[-1].get('path') or 'update' in args[-1].get('path'):
                        if data.get('db') in cound_list:
                            return fuc(*args)
                        else:
                            return {
                                "code": NOT_ALLOW,
                                "msg": '没有权限修改该数据库1',
                                "data": []
                            }
                    return fuc(*args)
                else:
                    return {
                        "code": NOT_ALLOW,
                        "msg": '没有权限查看该数据库2',
                        "data": []
                    }
            if data.get('db') in cound_list:
                return fuc(*args)
            else:
                return {
                    "code": NOT_ALLOW,
                    "msg": '没有权限查看该数据库3',
                    "data": []
                }
        except Exception:
            pass

    return wrapTheFunction
