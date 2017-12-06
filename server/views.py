from django.shortcuts import render
from django.http import JsonResponse, HttpResponse

from .spider import spider_main
import json
import urllib.parse as urlparse
from . import models


# Create your views here.

def getGuitarSheet(request):
    configParam = models.ConfigParam()
    if request.body:
        bodyStr = str(request.body, 'utf-8')
        jsonStr = urlparse.unquote(bodyStr)
        # print("\n request.body:", jsonStr, "-", type(request))
        data = json.loads(jsonStr.split('=')[1].replace('+', ' '))
        # print('data:', data)
        configParam.macAddress = data['macAddress']
        configParam.rootUrl = data['rootUrl']
        configParam.urlTag = data['urlTag']
        configParam.pageTitle = data['pageTitle']
        configParam.pageClass = data['pageClass']
        configParam.objClass = data['objClass']
        configParam.objTagClass = data['objTagClass']
        configParam.filter = data['filter']

    else:
        configParam.macAddress = 'aa.bb.cc.dd'
        configParam.rootUrl = 'http://www.17jita.com'
        configParam.urlTag = 'base'
        configParam.pageTitle = '吉他谱'
        configParam.pageClass = 'pg'
        configParam.objClass = 'xi2'
        configParam.objTagClass = 'bm_c xld'
        configParam.filter = ''
        configParam.action = 'ACTION_GET_SHEET'

    configParam.save()

    # return None
    spider = spider_main.SpiderManager()

    jsonDict = spider.craw(configParam)

    dataJson = json.dumps(jsonDict)
    print(dataJson)
    if request.method == 'GET':
        resp = HttpResponse(dataJson, content_type="application/json")
        return resp
    else:
        resp = HttpResponse(dataJson, content_type="application/json")
        return resp


def getSheetImg(request):
    configParam = models.ConfigParam()
    if request.body:
        bodyStr = str(request.body, 'utf-8')
        jsonStr = urlparse.unquote(bodyStr)
        data = json.loads(jsonStr.split('=')[1].replace('+', ' '))
        configParam.rootUrl = data['rootUrl']
        configParam.macAddress = data['macAddress']
        configParam.action = data['action']
        configParam.save()
        if not configParam.rootUrl:
            return HttpResponse('url is null！', content_type="application/text")
    else:
        return HttpResponse('request body is null！', content_type="application/text")

    spider = spider_main.SpiderManager()
    jsonDict = spider.getImgLinks(configParam.rootUrl)
    print(jsonDict)
    if jsonDict:
        dataJson = json.dumps(jsonDict)
    else:
        return HttpResponse('get nothing！', content_type="application/text")
    if request.method == 'POST':
        resp = HttpResponse(dataJson, content_type="application/json")
        return resp
    else:
        return HttpResponse('illegal request！', content_type="application/json")
