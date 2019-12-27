import csv
import re
import time

import jieba
import os
from similarity import Similarity
from synonym import Synonym
from api_controller import APIcontroller


class MyBot:
    def __init__(self, filename, keys, name, sex, age, school, city, height, weight):
        self.filename = filename    # 知识库路径
        self.name, self.sex, self.age, self.school, self.city, self.height, self.weight = name, sex, age, school, city, height, weight      # 机器人信息赋值
        self.synonym = Synonym("synonym.csv")   # 同义词库
        self.controller = APIcontroller(keys)       # API控制器
        self.help = '你可以用这些小工具哦：\n' \
                    '1.@百科 查询名词\n' \
                    '2.@天气 地名\n' \
                    '3.@日期\n' \
                    '4.@笑话\n' \
                    '5.@新闻头条\n' \
                    '6.@微信精选\n' \
                    '7.@邮编查询 邮编\n' \
                    '8.@繁简火星文切换 句子\n' \
                    '9.@新华字典 字\n' \
                    '10.@成语词典 成语\n' \
                    '11.@QQ号码测吉凶 QQ号\n' \
                    '12.help\n' \
                    '要按格式来哦，不然我会当做闲聊的啦'
        # 机器人信息
        self.info = None
        self.update_bot_info()

        self.not_ans = ['我好像没法理解你在说什么哦',
                        '找不到答案哦']
        # 自动回复数据表
        if not os.path.exists(filename):
            with open(filename, 'w', encoding='UTF-8'):
                pass
        with open(filename, 'r', encoding='UTF-8') as file:
            self.database = list(csv.reader(file))
        print('我醒了！\n' + self.help)

    def update_bot_info(self):
        # 机器人信息
        self.info = [["你的名字是什么", "我是" + self.name],
                     ["你叫什么", "我是" + self.name],
                     ["你是什么人", "我是" + self.name],
                     ["你的性别是什么", "我是" + self.sex + "的"],
                     ["你是男的女的", "我是" + self.sex + "的"],
                     ["你的年龄多大", "我" + self.age + "岁"],
                     ["你多大", "我" + self.age + "岁"],
                     ["你贵庚", "我" + self.age + "岁"],
                     ["你几岁了", "我" + self.age + "岁"],
                     ["你多老了", "我" + self.age + "岁"],
                     ["你是什么学校的", "我是" + self.school + "的"],
                     ["你哪个学校的", "我是" + self.school + "的"],
                     ["你在哪个城市", "我在" + self.city],
                     ["你在哪", "我在" + self.city],
                     ["你身高多少", "我身高" + self.height + "cm"],
                     ["你多高", "我身高" + self.height + "cm"],
                     ["你多重", "我体重" + self.weight + "kg"],
                     ["你体重多少", "我体重" + self.weight + "kg"]]


    # 输入
    def ask(self, sentence):
        sentence = sentence.strip()
        ans = self.find(sentence)
        if ans != 0 and ans != 1:
            return ans
        return self.not_ans[ans]


    # 找答案
    def find(self, sentence):

        if sentence == '':
            return '你怎么不说话呢'

        if sentence == 'help':
            return self.help

        if sentence[0] == '@':
            splits = sentence.split()
            if len(splits) > 1:
                res = self.controller.control(splits[0][1:], splits[1])
            else:
                res = self.controller.control(splits[0][1:], '')
            if res is False:
                return 1
            else:
                return res

        res = self.compare(sentence)
        if res is not False:
            return res

        search_names = [sentence]
        sentence = sentence.replace('啊', '').replace('哦', '').replace('嗯', '').replace('吧', '').replace('你', '').\
            replace('我', '').replace('他', '').replace('她', '').replace('它', '').replace('是', '').replace('不', '')
        search_names = search_names + self.cut(sentence)
        # print(search_names)
        for word in search_names:
            text = self.controller.search(word)
            if text is not False:
                return '我猜你想问:' + text
        return 0

    def compare(self, sentence):
        start = time.time()
        words = self.cut(sentence)
        # print(words)
        for word in [sentence] + words:
            sentences = self.synonym.replace(word, sentence)
            # print(sentences)
            for sen in sentences:
                # print(sen)
                for item in self.info + self.database:
                    # print(item)
                    # print(Similarity.get_cos_similarity(sen, item[0]))
                    if time.time() - start > 30:
                        return False
                    if Similarity.get_cos_similarity(sen, item[0]) > 0.65:
                        return item[1]
        return False

    # 分词
    @staticmethod
    def cut(sentence):
        words = [i for i in jieba.cut(sentence, cut_all=True) if i != '']  # 分词结果
        return words

    # 学习QQ聊天记录
    def learn(self, filename):
        knowledge = []
        with open(filename, 'r', encoding='utf-8') as file:
            line = ''
            while True:
                lastline = line
                line = file.readline()
                if not line:
                    break
                if re.search('\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', line) is not None:
                    text = self.__get_sentence(file)
                    if text is False:
                        continue
                    if re.sub('\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', '', line) != \
                            re.sub('\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', '', lastline):
                        knowledge.append([text])
                    else:
                        knowledge.append(knowledge.pop() + [text])
        print(knowledge)
        """
        self.add_all(knowledge)
        self.update_to_file()
        """
        return True

    def __get_sentence(self, file):
        sentence = ''
        while True:
            line = file.readline().strip()
            if not line:
                break
            line = line.replace('[图片]', '').replace('[表情]', '').replace(',', '，')
            if line == '':
                break
            sentence = sentence + line
        if sentence != '':
            print(sentence)
            return sentence
        return False

    def add_all(self, knowledge):
        for i in range(len(knowledge)-1):
            for q in knowledge[i]:
                for a in knowledge[i+1]:
                    self.add_one([q, a])
        return True

    def add_one(self, new):
        self.database.append(new)
        return True

    def delete(self, index):
        try:
            return self.database.pop(index)
        except IndexError:
            return False

    def update(self, index, new):
        if index >= len(self.database):
            return False
        self.database[index] = new
        return True

    def update_to_file(self):
        if self.database is not None:
            with open(self.filename, 'w', newline='', encoding='UTF-8') as file:
                writer = csv.writer(file)
                for row in self.database:
                    writer.writerow(row)
                return True
        return False
