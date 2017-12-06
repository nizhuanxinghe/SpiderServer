from bs4 import BeautifulSoup
import re
import urllib.parse as urlparse
from .downloader import HtmlDownloader


class HtmlParser(object):
    def parseSheetList(self, page_url, html_con, config_param):
        if page_url is None or html_con is None:
            return

        soup = BeautifulSoup(html_con, 'html.parser')
        new_data = self._get_new_data(soup, config_param)
        return new_data

    # def _get_new_urls(self, page_url, soup):
    #     new_urls = set()
    #     # /view/123.htm
    #     links = soup.find_all('a', href=re.compile(r'/view/\d+\.htm'))
    #     for link in links:
    #         new_url = link['href']
    #         new_full_url = urlparse.urljoin(page_url, new_url)  # join url
    #         new_urls.add(new_full_url)
    #
    #     return new_urls

    def _get_new_data(self, soup, config_param):

        res_data = {}

        print(config_param)

        url_tag = config_param.urlTag  # <head><base href="http://www.17jita.com/"><head> : base

        base_url = soup.find('head').find(url_tag).get('href')

        print('base_url:', base_url)

        page_title = config_param.pageTitle  # 吉他谱 通过这个的到目标html的page href

        page_url = soup.find('body').find(title=page_title).get('href')

        print('page_url:', page_url)

        downloader = HtmlDownloader()

        content = BeautifulSoup(downloader.download(page_url), 'html.parser')

        page_class = config_param.pageClass  # 'pg'

        page_ctr = content.find('body').find(class_=page_class)

        print('page_ctr:', page_ctr)

        page_url_list = []  # 所有谱子页面的url

        page_url_list.append(page_url)

        pages = page_ctr.find_all('a')

        for page in pages:
            print(page.get('href'))
            page_url_list.append((page.get('href')))

        obj_class = config_param.objClass  # 'xi2'
        obj_tab_class = config_param.objTagClass
        print('obj_class:', obj_class)
        print('obj_tab_class:', obj_tab_class)

        data_list = []
        for pageUrl in page_url_list:
            content = BeautifulSoup(downloader.download(pageUrl), 'html.parser')
            data_list = data_list + content.find('body').find(class_=obj_tab_class).find_all(class_=obj_class)

        # print('data_list:', data_list)
        res_data['base_url'] = base_url
        res_data['data_list'] = data_list
        return res_data

    def parseImg(self, html_con):
        picture_list = []
        if html_con is None:
            return

        soup = BeautifulSoup(html_con, 'html.parser')
        # body = soup.find('body').find_all('img')
        # print('body:', body)
        picture_list = soup.find_all('img')
        print(picture_list)

        return picture_list
