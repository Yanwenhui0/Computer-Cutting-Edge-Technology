from urllib import request
from urllib import parse
from bs4 import BeautifulSoup
import csv
import json
import re
import time


class APIcontroller:

    def __init__(self, keys):
        self.citycodes = []
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
                                      'like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
        self.keys = keys

    # APIs
    def control(self, method, sentence):
        # print('method=' + method + ' sentence=' + sentence)
        if sentence == '':
            if method == '日期':
                return self.date()
            elif method == '笑话':
                return self.joy()
            elif method == '新闻头条':
                return self.news()
            elif method == '微信精选':
                return self.chose()
        else:
            if method == '百科':
                return self.search(sentence)
            elif method == '天气':
                return self.weather(sentence)
            elif method == '邮编查询':
                return self.postcode(sentence)
            elif method == '新华字典':
                return self.dictionary(sentence)
            elif method == '成语词典':
                return self.idiom(sentence)
            elif method == 'QQ号码测吉凶':
                return self.qqnum(sentence)
        return False

    # 微信精选
    def chose(self):
        url = 'http://v.juhe.cn/weixin/query?key=' + self.keys[7]

        response = request.Request(url, headers=self.headers)
        obj = json.loads(request.urlopen(response).read().decode('utf-8'))
        # print(obj)
        if obj['result']['list'] is not None:
            return obj['result']['list'][0]['title'] + '\n' + obj['result']['list'][0]['url']
        return False

    # 新闻头条
    def news(self):
        url = 'http://v.juhe.cn/toutiao/index?type=top&key=' + self.keys[6]
        response = request.Request(url, headers=self.headers)
        obj = json.loads(request.urlopen(response).read().decode('utf-8'))
        # print(obj)
        if obj['result']['data'] is not None:
            return obj['result']['data'][0]['title'] + '\n' + obj['result']['data'][0]['url']
        return False

    # 笑话
    def joy(self):
        url = 'http://v.juhe.cn/joke/content/list.php?key=' + self.keys[5] + '&page=1&pagesize=1&sort=desc&time=' \
              + str(int(time.time()))
        response = request.Request(url, headers=self.headers)
        obj = json.loads(request.urlopen(response).read().decode('utf-8'))
        # print(obj)
        if obj['result']['data'] is not None:
            return obj['result']['data'][0]['content']
        return False

    # QQ号码测吉凶
    def qqnum(self, sentence):
        url = 'http://japi.juhe.cn/qqevaluate/qq?key=' + self.keys[4] + '&qq=' + sentence
        response = request.Request(url, headers=self.headers)
        obj = json.loads(request.urlopen(response).read().decode('utf-8'))
        if obj['error_code'] == 0:
            return obj['result']['data']['conclusion'] + '\n' + obj['result']['data']['analysis']
        return False

    # 成语词典
    def idiom(self, sentence):
        text = '简解：\n'
        url = 'http://v.juhe.cn/chengyu/query?key=' + self.keys[3] + '&word=' + parse.quote(sentence)
        response = request.Request(url, headers=self.headers)
        obj = json.loads(request.urlopen(response).read().decode('utf-8'))
        if obj['result'] is not None:
            return text + obj['result']['chengyujs']
        return False

    # 新华字典
    def dictionary(self, sentence):
        text = '简解：\n'
        url = 'http://v.juhe.cn/xhzd/query?key=' + self.keys[2] + '&word=' + parse.quote(sentence)
        response = request.Request(url, headers=self.headers)
        obj = json.loads(request.urlopen(response).read().decode('utf-8'))
        if obj['result'] is not None:
            list = obj['result']['jijie']
            for p in list:
                text = text + p + ' '
            return text
        return False

    # 邮编查询
    def postcode(self, sentence):
        url = 'http://v.juhe.cn/postcode/query?postcode=' + sentence + '&key=' + self.keys[0]
        response = request.Request(url, headers=self.headers)
        obj = json.loads(request.urlopen(response).read().decode('utf-8'))
        if obj['result']['list'] is not None:
            text = obj['result']['list'][0]['Province'] + obj['result']['list'][0]['City'] + obj['result']['list'][0][
                'District']
            return text
        return False

    # 天气
    def weather(self, city):
        with open("mybot/citycode.csv", 'r', encoding='UTF-8') as file:
            self.citycodes = list(csv.reader(file))
        for citydict in self.citycodes:
            if citydict[0] in city:
                url = 'http://t.weather.sojson.com/api/weather/city/' + citydict[1]
                response = request.Request(url, headers=self.headers)
                obj = json.loads(request.urlopen(response).read().decode('utf-8'))
                if obj['status'] == 200:
                    text = obj['cityInfo']['city'] + '天气：\n今天是{ymd}，{week}，{type}，最{high}，最{low}，空气质量指数 {aqi}，{fx} {' \
                                                     'fl}，日出时间 {sunrise}，{notice}。'.format(**obj['data']['forecast'][0])
                    return text
        return False

    # 日期查询
    @staticmethod
    def date():
        return '今天是' + time.strftime("%Y/%m/%d", time.localtime())

    # 链接百度百科
    def search(self, word):
        url = 'https://baike.baidu.com/search/word?word=' + parse.quote(word)
        page = request.Request(url, headers=self.headers)
        page_info = request.urlopen(page).read().decode('utf-8')
        # print(page_info)
        soup = BeautifulSoup(page_info, 'html.parser')
        tot = soup.find('div', 'lemma-summary')
        if tot is None:
            return False
        text = tot.get_text().replace('\r', '').replace('\n', '')
        text = re.sub(r'\[\d+\]', '', text)
        text = re.sub(r'\[\d+-\d+\]', '', text)
        return word + '\n' + text
