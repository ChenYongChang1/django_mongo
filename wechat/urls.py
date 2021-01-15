# -*- coding:utf8 -*-

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^appid', views.get_app_id),
    url(r'openid', views.get_open_id),
    url(r'getsign', views.getSign)
]