from bs4 import BeautifulSoup
import re
import urllib.parse as urlparse


class HtmlParser(object):
    def parse(self, page_url, html_cont):
        if page_url is None or html_cont is None:
            return

        soup = BeautifulSoup(html_cont, 'html.parser')
        new_urls = self._get_new_urls(page_url, soup)
        new_data = self._get_new_data(page_url, soup)
        return new_urls, new_data

    def _get_new_urls(self, page_url, soup):
        new_urls = set()
        # /view/123.htm
        links = soup.find_all('a', href=re.compile(r'/view/\d+\.htm'))
        for link in links:
            new_url = link['href']
            new_full_url = urlparse.urljoin(page_url, new_url)  # join url
            new_urls.add(new_full_url)

        return new_urls

    def _get_new_data(self, page_url, soup):
        res_data = {}

        # url
        res_data['url'] = page_url

        base_url = soup.find('head').find('base').get('href')
        data_list = soup.find('body', id="nv_portal") \
            .find('div', class_='bm_c xld').find_all('a', target="_blank")

        i = 0
        for a in data_list:
            i = i + 1
            print(i, "-", a.get('href'), "-", a.string)

        res_data['base_url'] = base_url
        res_data['data_list'] = data_list
        return res_data
