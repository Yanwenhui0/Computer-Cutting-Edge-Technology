from django.shortcuts import render
from mybot.my_bot import MyBot
import numpy


numpy.seterr(divide='ignore', invalid='ignore')
keys = ['邮编查询',                 """记得删除"""
		'繁简火星文切换(已删)',
		'新华字典',
		'成语词典',
		'QQ号码测吉凶',
		'笑话',
		'新闻头条',
		'微信精选']
myBot = MyBot("mybot/datas.csv", keys, "Jeff", "男", "18",  "华东师范大学", "上海", "178", "60")

def index(request):

	content = {}
	if 'q' in request.GET:
		content['answer'] = myBot.ask(request.GET['q'])
	else:
		content['answer'] = myBot.not_ans[0]
	return render(request, 'index.html', content)

