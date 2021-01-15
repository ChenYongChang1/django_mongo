from init.mongo_init import Mongdb
import time
from config.error_config import LOGIN_ERROR, LOGIN_FORBIDDEN, SUCCESS


class Login(Mongdb):
    def __init__(self):
        super(Login, self).__init__('admin_user')

    def login(self, info):
        name, pwd = info.get('name'), info.get('password')
        if not name or not pwd:
            raise Exception(LOGIN_ERROR)
        result = list(
            self.db['user'].find({
                "userName": name,
                "pwd": pwd
            })
        )
        print(result)
        if len(result) and result[0]['userName'] == name and result[0]['pwd'] == pwd:
            times = time.time()
            if result[0].get('superAdmin') or \
                    str(result[0].get('flag')) == '1' \
                    and int(result[0].get('startTime')) / 1000 < times < int(result[0].get('endTime')) / 1000:
                result[0].pop('pwd')
                result[0].pop('_id')
                result[0].pop('endTime')
                result[0]['assToken'] = self.setToken({
                    'name': result[0]['userName'],
                    'cound': result[0]['cound'],
                    'type0': result[0].get('type0'),
                    'superAdmin': result[0].get('superAdmin'),
                })
                return self.responseContent(SUCCESS, '登录成功', result[0])
            else:
                return self.responseContent(LOGIN_FORBIDDEN, '已被限制登陆', {})
        else:
            return self.responseContent(LOGIN_ERROR, '登录失败', {})
