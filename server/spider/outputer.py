

class HtmlOutput(object):
    def __init__(self):
        self.datas = {}
        self.base_url = ''

    def collect_data(self, data):
        if data is None:
            return
        self.datas = data['data_list']
        self.base_url = data['base_url']

    def output_txt(self):

        fout = open('output.txt', 'w')
        fout.write("{\n\"dataList\":[")
        for data in self.datas:
            fout.write("\n{\"link\":\"%s\",\"title\":\"%s\"}," % (
                "%s%s" % (self.base_url, data.get('href')), data.string))
        fout.write("\n]\n}")
        fout.close()

        return fout
