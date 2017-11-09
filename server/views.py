from django.shortcuts import render
from django.http import JsonResponse, HttpResponse

from .spider import spider_main
from . import models
import json


# Create your views here.

def getGuitarSheet(request):
    spider = spider_main.SpiderMain()
    root_url = "http://www.17jita.com/tab/"
    jsonDict = spider.craw(root_url)
    if request.body:
        data = json.load(request.body)

    print(jsonDict)
    dataJson = json.dumps(jsonDict)
    print(dataJson)
    if request.method == 'GET':
        resp = HttpResponse(dataJson, content_type="application/json")
        return resp
    else:
        return
