from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^data', views.add_data),
    url(r'^count', views.add_count),
    url(r'^article', views.add_other_article),
    url(r'^sign', views.get_sign_oss)
]
