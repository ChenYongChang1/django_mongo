from django.conf.urls import url
from . import views

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^deleteone', views.delete_data),
    url(r'^drop', views.drop),
]