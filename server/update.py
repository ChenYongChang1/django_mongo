from config.reg_config import reg
from init.mongo_init import Mongdb
from util.auth import check_auth,checkDeleAuth
import re
from bson.objectid import ObjectId
from config.error_config import SUCCESS, ACTION_LOSE

# 修改数据
class updateObj(Mongdb):
    def __init__(self, db, *table):
        try:
            self.table = table[0]
            print('table', table[0])
        except Exception:
            pass
        super(updateObj, self).__init__(db)

    @checkDeleAuth
    @check_auth
    def updataMess(self, data):
        # for j in data.get('query'):
        #     if "_id" == j:
        #         data['query'][j] = ObjectId(data['query'][j])
        #     if 'queryType' in data and data.get('queryType') == 1:
        #         if "_id" != j:
        #             data['query'][j] = re.compile(data['query'][j])
        for i in data['query']:
            if "_id" == i:
                data['query'][i] = ObjectId(data['query'][i])
                break
            if '$' in i:
                for keyObj in data['query'][i]:
                    for key in keyObj:
                        val = re.findall(reg, keyObj[key])
                        if val and len(val):
                            keyObj[key] = re.compile(val[0])
            else:
                val = re.findall(reg, data['query'][i])
                if val and len(val):
                    data['query'][i] = re.compile(val[0])
        data.get('query')['isdelete'] = {'$ne': True}
        try:
            rest = self.db[self.table].update_many(data.get('query'),
                                                   {'$set': data.get('jsonMessage')})
        except Exception:
            return self.responseContent(ACTION_LOSE, '修改异常', {})
        return self.responseContent(SUCCESS, '修改成功', data)

