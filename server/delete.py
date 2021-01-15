# -*- coding:utf8 -*-
from bson import ObjectId

from init.mongo_init import Mongdb
from util.auth import check_auth, checkDeleAuth
from config.error_config import SUCCESS, ACTION_LOSE, BAD_PARAMS
import re


class DeleObj(Mongdb):
    def __init__(self, db, *table):
        try:
            self.table = table[0]
            print('table', table[0])
        except Exception:
            pass
        super(DeleObj, self).__init__(db)

    def useTokenGetData(self, token):
        coundList = self.openToken(token).get('message').get('cound')
        adminpeople = self.openToken(token).get('message').get('type0')
        superAdmin = self.openToken(token).get('message').get('superAdmin')
        return coundList, superAdmin, adminpeople

    @checkDeleAuth
    @check_auth
    def deleData(self, data):
        if 'jsonMessage' not in data:
            raise Exception(BAD_PARAMS)
        for i in data['jsonMessage']:
            if "_id" == i:
                data['jsonMessage'][i] = ObjectId(data['jsonMessage'][i])
        if 'queryType' in data and data.get('queryType') == 1:
            try:
                for i in data['jsonMessage']:
                    if "_id" != i:
                        data['jsonMessage'][i] = re.compile(data['jsonMessage'][i])
            except Exception:
                pass
        rest = self.db[self.table].delete_many(data['jsonMessage'])
        return self.responseContent(SUCCESS, '删除成功', rest.deleted_count or '0')

    @checkDeleAuth
    @check_auth
    def dropData(self, data):
        try:
            self.db[self.table].drop()
            return self.responseContent(SUCCESS, '删除成功', {'table': self.table})
        except Exception:
            return self.responseContent(ACTION_LOSE, '', {})
