from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'getGuitarSheet', views.getGuitarSheet, name='getGuitarSheet'),
    url(r'getSheetImg', views.getSheetImg, name='getSheetImg')
]
