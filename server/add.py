import uuid
import time
import random
# from qiniu import Auth
from server.spider import get_acticle
from util.auth import check_auth
from util.ossSign import get_token
from init.mongo_init import Mongdb

from config.error_config import SUCCESS, ACTION_LOSE, CAN_NOT_GET_RESOURCE
import re


# 增加数据
class addObj(Mongdb):
    def __init__(self, db, *table):
        try:
            self.table = table[0]
            print('table', table[0])
        except Exception:
            pass
        super(addObj, self).__init__(db)

    @check_auth
    def addData(self, data):
        try:
            rest = self.db[self.table].insert_one(data.get('jsonMessage'))
            if rest.inserted_id:
                return self.responseContent(SUCCESS, '添加成功', data.get('jsonMessage'))
        except Exception:
            pass
        return self.responseContent(ACTION_LOSE, '操作失败', {})

    # @check_auth
    # def addDataPhoto(self, data):
    #     ''' 七牛云 '''
    #     try:
    #         # 需要填写你的 Access Key 和 Secret Key
    #         access_key = 'WhJ8pvZqhWMiia68KAzpRHV2bs-V9FvocnciNS4u'
    #         secret_key = '8vNNqGTLekq9opBJmDugDeJTeseyUYh-sinDPNZN'
    #         # userphone = request.GET.get('userphone')
    #         hz = data['jsonMessage']['hz'] if 'hz' in data['jsonMessage'] else 'jpg'
    #         filename = str(int(time.time())) + str(int(random.random() * 100000)) + '.' + hz
    #         print(filename)
    #         # 构建鉴权对象
    #         q = Auth(access_key, secret_key)
    #         # 要上传的空间
    #         bucket_name = data['jsonMessage']['kongjian']
    #         key = str(uuid.uuid4()) + '.' + filename.split('.')[-1]
    #         # 生成上传 Token，可以指定过期时间等
    #         token = q.upload_token(bucket_name, key, 3600)
    #         domain = data['jsonMessage']['domain']
    #         print({"uptoken": token, "domain": domain, "key": key})
    #         return self.responseContent(SUCCESS, '获取成功',
    #                                     {"uptoken": token, "domain": domain, "kongjian": bucket_name, "key": key})
    #     except Exception:
    #         return self.responseContent(ACTION_LOSE, '操作失败', {})


@check_auth
def get_oss(data):
    oss_signs = get_token(data.get('dir'))
    return {
        "code": SUCCESS,
        "msg": '获取成功',
        "data": oss_signs
    }


@check_auth
def add_other_resourse(data):
    try:
        article_html = get_acticle(data.get('jsonMessage'))
    except Exception:
        article_html = ''
    if not article_html:
        raise Exception(CAN_NOT_GET_RESOURCE)
    return article_html
