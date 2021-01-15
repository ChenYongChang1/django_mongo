import random
import time

import requests
from lxml import etree
from lxml.html import tostring

from config.error_config import HAVE_NO_RESOURCE
from config.spider_config import FROM_RESOURCE_DICT


def get_html(url, row_resource):
    user_agent = [
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0',
        'Opera/9.80 (Windows NT 6.1; U; zh-cn) Presto/2.9.168 Version/11.50',
        'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'
    ]
    user_choose = random.choice(user_agent)
    headers = {
        'User-Agent': user_choose,
        'Referer': row_resource.get('rerfer') or 'https://baidu.com',
        'Sec-Fetch-Mode': 'no-cors'
    }
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        time.sleep(1)
        return get_html(url, row_resource)
    r.encoding = 'utf-8'
    return r


def get_acticle(data):
    url = data.get('url')
    from_resource = data.get('resource')
    row_resource = FROM_RESOURCE_DICT.get(from_resource) or ''
    if not row_resource or type(row_resource) == 'str':
        raise Exception(HAVE_NO_RESOURCE)
    r_article = get_html(url, row_resource)
    code = r_article.apparent_encoding  # 获取url对应的编码格式
    content_html = etree.HTML(r_article.text)
    try:
        title_html = content_html.xpath('//title//text()')[0]
    except Exception as e:
        title_html = '未获取到标题'
    data_html = tostring(content_html.xpath(row_resource.get('xpath'))[0], encoding=code).decode(code)
    return data_html, title_html
