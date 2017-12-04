from bs4 import BeautifulSoup
import re
import urllib.parse as urlparse
from .downloader import HtmlDownloader


class HtmlParser(object):
    def parse(self, page_url, html_cont, configParam):
        if page_url is None or html_cont is None:
            return

        soup = BeautifulSoup(html_cont, 'html.parser')
        new_data = self._get_new_data(soup, configParam)
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

    def _get_new_data(self, soup, configParam):

        res_data = {}

        print(configParam)

        url_tag = configParam.urlTag  # <head><base href="http://www.17jita.com/"><head> : base

        base_url = soup.find('head').find(url_tag).get('href')

        print('base_url:', base_url)

        page_title = configParam.pageTitle  # 吉他谱 通过这个的到目标html的page href

        page_url = soup.find('body').find(title=page_title).get('href')

        print('page_url:', page_url)

        downloader = HtmlDownloader()

        content = BeautifulSoup(downloader.download(page_url), 'html.parser')

        page_class = configParam.pageClass  # 'pg'

        page_ctr = content.find('body').find(class_=page_class)

        print('page_ctr:', page_ctr)

        page_url_list = []  # 所有谱子页面的url

        page_url_list.append(page_url)

        pages = page_ctr.find_all('a')

        for page in pages:
            print(page.get('href'))
            page_url_list.append((page.get('href')))

        obj_class = configParam.objClass  # 'xi2'
        obj_tab_class = configParam.objTagClass
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
