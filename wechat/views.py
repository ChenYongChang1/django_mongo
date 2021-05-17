from django.shortcuts import render
from django.http import response, request, HttpResponse, JsonResponse
from config.config import WECHART_CONFIG
import json, requests, time, redis
from bson import json_util
from config.config import REDIS_CONFIG
from config.error_config import SUCCESS, OLD_CODE, AUTH_ERROR
from init.return_res import http_response


class RedisReadWrite:
    def __init__(self):
        pool = redis.ConnectionPool(host=REDIS_CONFIG.get('host'), port=REDIS_CONFIG.get('port'), db=1,
                                    password=REDIS_CONFIG.get('auth'), decode_responses=True)
        self.redis = redis.Redis(connection_pool=pool)

    def writeRedis(self, jsapi_ticket):
        # self.redis.set('proxy',info)
        self.redis.set("jsapi_ticket", jsapi_ticket, 7100)

    def getRedis(self):
        # return self.redis.get('proxy')
        jsapi_ticket = self.redis.get("jsapi_ticket")
        return jsapi_ticket

    def deleteProxy(self, key):
        self.redis.hdel("proxy", key)


redis_db = RedisReadWrite()


# @checkMethod
def get_app_id(request):
    return http_response(WECHART_CONFIG['appId'], SUCCESS)

def getAuth(request):
    print(request.GET)
    return HttpResponse(request.GET.get('echostr'))# http_response(WECHART_CONFIG['appId'], SUCCESS)

def get_open_id(request):
    code = request.GET.get('code')
    r = requests.get(
        'https://api.weixin.qq.com/sns/oauth2/access_token?appid=' + WECHART_CONFIG['appId'],
        '&secret=' + WECHART_CONFIG['secret'] + '&code=' + code + '&grant_type=authorization_code')
    objopenid = r.json()
    if objopenid.get('errcode') == 40163 or objopenid.get('errcode') == 40029:
        return http_response('', OLD_CODE, 'code已被使用:{}'.format(objopenid.get('errcode')))
    return http_response(objopenid, SUCCESS)


def cacheticket():
    r = requests.get(
        'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}'.format(
            WECHART_CONFIG['appId'],
            WECHART_CONFIG['secret']
        ))
    token = json.loads(r.text)
    if token.get('errcode') == 45009:
        print('过期')
        return '1'
    r2 = requests.get(
        'https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token={}&type=jsapi'.format(
            token.get('access_token')))
    jsapi_ticket = json.loads(r2.text).get('ticket')
    return jsapi_ticket if jsapi_ticket else ''


def createNonceStr():
    import random
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    str = ""
    for i in range(0, 16):
        s = random.randint(0, len(chars) - 1)

        str += chars[s:s + 1]
    return str


def getSign(request):
    jsapi_ticket_list = redis_db.getRedis()
    if jsapi_ticket_list and len(jsapi_ticket_list) > 0:
        try:
            jsapi_ticket = jsapi_ticket_list
            if not jsapi_ticket:
                jsapi_ticket = setjsapi_ticket()
        except Exception as e:
            print(e)
            jsapi_ticket = setjsapi_ticket()
    else:
        jsapi_ticket = setjsapi_ticket()
    if jsapi_ticket:
        import hashlib
        # 'http://27400o9p74.zicp.vip'
        # url = "{}://{}{}".format(request.protocol, request.host, request.uri)
        url = request.META['HTTP_REFERER']
        timestamp = int(time.time())
        nonce = createNonceStr()
        ret = {
            "noncestr": nonce,
            "jsapi_ticket": jsapi_ticket,
            "timestamp": timestamp,
            "url": url
        }
        temp = "&".join(['%s=%s' % (key.lower(), ret[key]) for key in sorted(ret)])
        sig = hashlib.sha1(temp.encode("utf8")).hexdigest()
        package = {
            "timestamp": timestamp,
            "nonceStr": nonce,
            "signature": sig,
            "appId": WECHART_CONFIG['appId'],
        }

        return http_response(package, SUCCESS)
    else:
        return http_response({
            "timestamp": '',
            "nonceStr": '',
            "signature": '',
            "appId": '',
            'code': '授权出错'
        }, AUTH_ERROR)


def setjsapi_ticket():
    ticket = cacheticket()
    # r = get_redis_connection("default")
    # r.set("jsapi_ticket", ticket if ticket else '', 7000)
    redis_db.writeRedis(ticket if ticket else '')
    return ticket if ticket else ''
