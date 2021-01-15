from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^dbs', views.dbs),
    url(r'^tables', views.query_table),
    url(r'^data', views.query_data),
    url(r'', views.demo),
]
