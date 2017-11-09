import requests


class HtmlDownloader(object):
    def download(self, url):
        if url is None:
            return None

        response = requests.get(url, allow_redirects=False)

        print("response.headers:", response.headers)
        print("response.encoding", response.encoding)
        # response.encoding = 'gb18030'  # 在解析之前进行编码格式指定,或者用esponse.content，解决乱码问题
        if response.status_code != 200:
            return None

        return response.content
