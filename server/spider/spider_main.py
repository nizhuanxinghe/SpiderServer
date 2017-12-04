from .. import models
from . import manager, downloader, parser, outputer


class SpiderMain(object):
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
        new_data = self.parser.parse(new_url, html_cont, configParam)

        self.outputer.collect_data(new_data)
        # self.outputer.output_txt()

        self.base_url = new_data['base_url']

        if new_data['data_list']:
            self.saveSheetToSql(new_data)
        return self.packData(models.GuitarSheet.objects.all(), configParam.filter)

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
