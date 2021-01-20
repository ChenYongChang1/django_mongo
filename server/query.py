from config.reg_config import reg
from init.mongo_init import Mongdb
from util.auth import check_auth
from config.error_config import SUCCESS, NOT_ALLOW, BAD_PARAMS
import re
from bson import json_util


class QueryObj(Mongdb):
    def __init__(self, db, *table):
        try:
            self.table = table[0]
            print('table', table[0])
        except Exception:
            pass
        super(QueryObj, self).__init__(db)

    def useTokenGetData(self, token):
        coundList = self.openToken(token).get('message').get('cound')
        adminpeople = self.openToken(token).get('message').get('type0')
        superAdmin = self.openToken(token).get('message').get('superAdmin')
        return coundList, superAdmin, adminpeople

    # 获取数据库列表
    def getDbs(self, token):
        coundList, superAdmin, adminpeople = self.useTokenGetData(token)
        printList = []
        if len(coundList) > 0:
            dbslists = self.client.list_database_names()
            if coundList[0] == 'all' or superAdmin or adminpeople:
                if not superAdmin:
                    'admin' in dbslists and dbslists.remove('admin')
                    'local' in dbslists and dbslists.remove('local')
                    'config' in dbslists and dbslists.remove('config')
                return self.responseContent(SUCCESS, '获取成功', dbslists)
            for i in coundList:
                if i in dbslists:
                    printList.append(i)
            return self.responseContent(SUCCESS, '获取成功', printList)
        else:
            return self.responseContent(NOT_ALLOW, '没有权限查看该数据库', [])

    # 获取数据库表的集合
    def getTable(self, token, db):
        coundList, superAdmin, adminpeople = self.useTokenGetData(token)
        tableList = self.db.list_collection_names()
        if superAdmin or adminpeople:
            return self.responseContent(SUCCESS, '获取成功', tableList)
        else:
            if db in coundList:
                return self.responseContent(SUCCESS, '获取成功', tableList)
        return self.responseContent(NOT_ALLOW, '没有权限查看该数据库', [])

    # 查看数据
    @check_auth
    def get_data(self, data):
        data['jsonMessage'] = data.get('jsonMessage', {})
        if not isinstance(data['jsonMessage'], dict):
            '''jsonmessage 必须的对象'''
            raise Exception(BAD_PARAMS)
        data['jsonMessage']['isdelete'] = {'$ne': True}
        # print(data.get('remove'), 'data')
        remove = data.get('remove') if data.get('remove') and len(data.get('remove')) else []
        remove.append('_id')
        if self.table == 'user':
            remove.append('password')
        remove_obj = dict(zip(remove, [0 for i in remove]))
        print(remove, remove_obj, 'remove_obj')
        # if 'queryType' in data and data.get('queryType') == 1:
        try:
            for i in data['jsonMessage']:
                if '$' in i:
                    print(data['jsonMessage'][i])
                    for keyObj in data['jsonMessage'][i]:
                        for key in keyObj:
                            val = re.findall(reg, keyObj[key])
                            if val and len(val):
                                keyObj[key] = re.compile(val[0])
                else:
                    val = re.findall(reg, data['jsonMessage'][i])
                    if val and len(val):
                        data['jsonMessage'][i] = re.compile(val[0])
        except Exception as e:
            pass
        if 'page' in data and 'pageSize' in data:
            start = (data['page'] - 1) * data['pageSize']
            size = self.db[self.table].find(data.get('jsonMessage'), remove_obj).count()
            if data.get('order'):
                order_row = data.get('order')
                '''order { orderBy: 字段名', isDesc: 1 / -1 } 必须的对象'''
                lists = self.db[self.table].find(data.get('jsonMessage'), remove_obj).sort(order_row['orderBy'],
                                                                                           self._order[order_row[
                                                                                               'isDesc']]).limit(
                    data['pageSize']).skip(start)
            else:
                lists = self.db[self.table].find(data.get('jsonMessage'), remove_obj).limit(data['pageSize']).skip(
                    start)
            mess = {
                "list": list(lists),
                "count": size,
                "page": data['page']
            }
        else:
            if data.get('order'):
                order_row = data.get('order')
                lists = self.db[self.table].find(data.get('jsonMessage'), remove_obj).sort(order_row['orderBy'],
                                                                                           self._order[
                                                                                               order_row['isDesc']])
            else:
                lists = self.db[self.table].find(data.get('jsonMessage'), remove_obj)
            mess = {
                'list': list(lists),
                'count': lists.count()
            }
        return self.responseContent(SUCCESS, '操作成功', mess)
