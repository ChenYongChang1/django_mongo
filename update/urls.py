from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^replace', views.update_data),
]
