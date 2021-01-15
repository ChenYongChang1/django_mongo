
import base64
import time
import datetime
import json
import hmac
from hashlib import sha1 as sha


# upload_dir = 'cyc-save/'
from config.config import access_key_secret, access_key_id, host

expire_time = 30


def get_iso_8601(expire):
    gmt = datetime.datetime.utcfromtimestamp(expire).isoformat()
    gmt += 'Z'
    return gmt


def get_token(upload_dir='cyc-save'):
    now = int(time.time())
    expire_syncpoint = now + expire_time
    expire_syncpoint = 1612345678
    expire = get_iso_8601(expire_syncpoint)
    policy_dict = {}
    policy_dict['expiration'] = expire
    condition_array = []
    array_item = []
    array_item.append('starts-with')
    array_item.append('$key')
    array_item.append(upload_dir)
    condition_array.append(array_item)
    policy_dict['conditions'] = condition_array
    policy = json.dumps(policy_dict).strip()
    policy_encode = base64.b64encode(policy.encode())
    h = hmac.new(access_key_secret.encode(), policy_encode, sha)
    try:
        sign_result = base64.encodestring(h.digest()).strip()
    except Exception as e:
        sign_result = ''.encode()
    token_dict = {}
    token_dict['accessid'] = access_key_id
    token_dict['host'] = host
    token_dict['policy'] = policy_encode.decode()
    token_dict['signature'] = sign_result.decode()
    token_dict['expire'] = expire_syncpoint
    token_dict['dir'] = upload_dir
    #result = json.dumps(token_dict)
    print('--------------------------------')
    return token_dict

# print(get_token())