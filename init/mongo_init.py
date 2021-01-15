from pymongo import MongoClient, ASCENDING, DESCENDING
import jwt
from datetime import datetime, timedelta
from config.config import MONGO_CONFIG
from config.error_config import REQUIRE_DB

SECRECT_KEY = 'cyc'


class Mongdb:
    def __init__(self, whichdb=''):
        self._order = {
            -1: DESCENDING,
            1: ASCENDING
        }
        if whichdb == '':
            raise Exception(REQUIRE_DB)
        self.client = MongoClient(MONGO_CONFIG['host'], MONGO_CONFIG['port'], username=MONGO_CONFIG['username'],
                                  password=MONGO_CONFIG['password'])
        try:
            self.db = self.client[whichdb]
        except Exception:
            pass
        if (self.client):
            print(self.client, '实例化成功')
        else:
            print('实例化失败')

    def setToken(self, name):
        datetimeInt = datetime.utcnow() + timedelta(hours=6)
        options = {
            'iss': 'chenyongchangdashuaibi',
            'exp': datetimeInt,
            'aud': 'webkit',
            'message': name
        }
        token = jwt.encode(options, SECRECT_KEY, 'HS256')
        return token

    def openToken(self, token):
        data = jwt.decode(token, SECRECT_KEY, audience='webkit', algorithms=['HS256'])
        return data

    def responseContent(self, code, mean, *data):
        return {
            "code": code,
            "msg": mean,
            "data": data[0] or ''
        }
