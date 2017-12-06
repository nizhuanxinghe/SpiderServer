from .. import models
from . import manager, downloader, parser, outputer


class SpiderManager(object):
    def __init__(self):
        self.urls = manager.UrlManager()
        self.downloader = downloader.HtmlDownloader()
        self.parser = parser.HtmlParser()
        self.outputer = outputer.HtmlOutput()
        self.base_url = ''

    def craw(self, configParam):
        self.urls.add_new_url(configParam.rootUrl)
        # while self.urls.has_new_url():
        new_url = self.urls.get_new_url()
        html_cont = self.downloader.download(new_url)
        new_data = self.parser.parseSheetList(new_url, html_cont, configParam)

        self.outputer.collect_data(new_data)
        # self.outputer.output_txt()

        self.base_url = new_data['base_url']

        if new_data['data_list']:
            self.saveSheetToSql(new_data)
        return self.packData(models.GuitarSheet.objects.all(), configParam.filter)

    def getImgLinks(self, url):
        html_con = self.downloader.download(url)
        data_list = self.parser.parseImg(html_con)
        if not data_list:
            return None
        for obj in data_list:
            if 'http' in obj.get('src'):
                img_href = obj.get('src')
            else:
                img_href = '%s%s' % (url, obj.get('src'))
            img_id = obj.get('id')
            title = obj.get('alt')
            existPics = models.Picture.objects.filter(link=img_href)
            if existPics:
                continue
            models.Picture.objects.create(link=img_href, picId=img_id, title=title)  #
        return self.packPicData(models.Picture.objects.all())

    def saveSheetToSql(self, datas):
        for obj in datas['data_list']:
            if self.base_url in obj:
                continue
            link = '%s%s' % (self.base_url, obj.get('href'))
            title = obj.string
            existedGuitarSheets = models.GuitarSheet.objects.filter(link=link)
            if existedGuitarSheets:
                continue
            # print('link:', link, ',title:', title, '\n')
            models.GuitarSheet.objects.create(link=link, title=title)

    def packData(self, datas, filter):
        # print('packData:', datas)
        jsonDict = {}
        dataList = []
        for obj in datas:
            # print('obj:', obj.link, obj.title)
            if filter.lower() not in obj.title.lower():
                continue
            data = {}
            data['id'] = obj.id
            data['link'] = obj.link
            data['title'] = obj.title
            dataList.append(data)
        jsonDict['dataList'] = dataList
        return jsonDict

    def packPicData(self, params):
        jsonDic = {}
        dataList = []
        for obj in params:
            data = {}
            data['picId'] = obj.picId
            data['link'] = obj.link
            data['title'] = obj.title
            dataList.append(data)
        jsonDic['dataList'] = dataList
        return jsonDic
