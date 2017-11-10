from django.shortcuts import render
from django.http import JsonResponse, HttpResponse

from .spider import spider_main
import json
import urllib.parse as urlparse


# Create your views here.

def getGuitarSheet(request):
    data = None
    if request.body:
        bodyStr = str(request.body, 'utf-8')
        jsonStr = urlparse.unquote(bodyStr)
        print("\n request.body:", jsonStr, "-", type(request))
        data = json.loads(jsonStr[5:])

    # return None
    spider = spider_main.SpiderMain()
    if data['rootUrl']:
        root_url = data['rootUrl']
    else:
        root_url = "http://www.17jita.com/tab/"

    jsonDict = spider.craw(root_url)

    dataJson = json.dumps(jsonDict)
    # print(dataJson)
    if request.method == 'GET':
        resp = HttpResponse(dataJson, content_type="application/json")
        return resp
    else:
        resp = HttpResponse(dataJson, content_type="application/json")
        return resp
