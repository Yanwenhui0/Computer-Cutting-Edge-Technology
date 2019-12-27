from mybot import MyBot
import numpy

numpy.seterr(divide='ignore', invalid='ignore')
keys = ['62db010514c88fed661c5d31601d74c7',                 """记得删除"""
        '11e65eeddd2f0dae54aed7bf1d61e6ae',
        '2c43fc68e4e76b3fd6cfe544f8d59301',
        '610892adff8075befeadf69ff2e81868',
        '9fc9d3f0ba66cd0556632c37e8525b11',
        '2028a83f812e09b1ce76a934c442c050',
        '4bf06ddad0733cc6806701c1faa5b71f',
        '67777c69bfda98cdc864aaba5a444891']
myBot = MyBot("datas.csv", keys, "Jeff", "男", "18",  "华东师范大学", "上海", "178", "60")

# myBot.learn('from.txt')

while True:
    print(myBot.ask(input('>>>')))





