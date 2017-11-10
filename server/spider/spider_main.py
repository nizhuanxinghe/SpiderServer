from .. import models
from . import manager, downloader, parser, outputer


class SpiderMain(object):
    def __init__(self):
        self.urls = manager.UrlManager()
        self.downloader = downloader.HtmlDownloader()
        self.parser = parser.HtmlParser()
        self.outputer = outputer.HtmlOutput()
        self.dataList = {}
        self.base_url = ''

    def craw(self, root_url):
        self.urls.add_new_url(root_url)
        # while self.urls.has_new_url():
        new_url = self.urls.get_new_url()
        html_cont = self.downloader.download(new_url)
        new_urls, new_data = self.parser.parse(new_url, html_cont)
        self.urls.add_new_urls(new_urls)

        self.outputer.collect_data(new_data)
        # self.outputer.output_txt()

        self.base_url = new_data['base_url']

        self.saveSheetToSql(new_data)

        return self.packData(models.GuitarSheet.objects.all())

    def saveSheetToSql(self, datas):
        for obj in datas['data_list']:
            link = '%s%s' % (self.base_url, obj.get('href'))
            title = obj.string
            existGuitarSheets = models.GuitarSheet.objects.filter(link=link)
            if existGuitarSheets:
                continue
            # print('link:', link, ',title:', title, '\n')
            models.GuitarSheet.objects.create(link=link, title=title)

    def packData(self, datas):
        # print('packData:', datas)
        jsonDict = {}
        dataList = []
        for obj in datas:
            # print('obj:', obj.link, obj.title)
            data = {}
            data['id'] = obj.id
            data['link'] = obj.link
            data['title'] = obj.title
            dataList.append(data)
        jsonDict['dataList'] = dataList
        return jsonDict

        # if __name__ == "__main__":

# root_url = "http://www.17jita.com/tab/"
#     obj_spider = SpiderMain()
#     obj_spider.craw(root_url)
