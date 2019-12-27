# MyBot

## File api_controller.py

### class APIcontroller

通过使用百度百科和聚合数据的免费API来查找答案
使用模块：urllib, bs4, csv, json, re, time

| 模块   | 功能                       |
| ------ | -------------------------- |
| urllib | 网络操作                   |
| bs4    | HTML解析                   |
| csv    | csv文件的读写              |
| json   | 实现json字符串和对象的转换 |
| re     | 正则表达式匹配             |

```python
__init__(keys[list of str])
	APIcontroller的初始化操作，导入用户的api_keys
		keys 聚合数据的API对应的AppKey
		return None
		
control(method[str], sentence[str]) -> bool
	控制器，选择相应的函数分支
		method API的类别，sentence 查询的对象
		return 是否查询出结果
		
date() -> str
	获取当前日期
		return 日期
		
joy(...) -> str
	利用urllib发出网络请求，通过json获取笑话
		return 笑话
		
news(...) -> str
	利用urllib发出网络请求，通过json获取新闻头条
		return 新闻头条

chose(...) -> str
	利用urllib发出网络请求，通过json获取微信精选
			return 微信精选

search(sentence[str]) -> str
	利用jieba分词，分出关键词，用urllib实现文本的url编码，并发出网络请求，用bs4解析HTML文本，获取简要信息，再用re对文本利用正则表达式进行过滤获取百度百科
		sentence 查询文本
		return 百科

weather(sentence[str]) -> str
	在网上找好中国天气网的API，预处理好城市码和城市的对应关系，通过csv进行文件读写，利用urllib发出网络请求，通过json获取天气
		sentence 查询文本
        return 天气

postcode(sentence[str]) -> str
	利用urllib发出网络请求，通过json获取邮编对应城市信息
		sentence 查询文本
		return 邮编查询

change(sentence[str]) -> str
	多次利用urllib对文本进行编码，并发出网络请求，再通过json获取文本，并整合
		sentence 查询文本
		return 繁简火星文切换

dictionary(sentence[str]) -> str
	利用urllib对文本进行编码，并发出网络请求，再通过json获取文本，并整合
		sentence 查询文本
		return 新华字典

idiom(sentence[str]) -> str
	利用urllib对文本进行编码，并发出网络请求，再通过json获取文本，并整合
		sentence 查询文本
		return 成语词典

qqnum(sentence[str]) -> str
	利用urllib对文本进行编码，并发出网络请求，再通过json获取文本，并整合
		sentence 查询文本
		return QQ号码测吉凶
```

## File mybot.py

### class MyBot

通过使用文本相似度算法和预处理过的QA数据库实现答案搜索, 并利用jieba分词，与近义词库进行比较。

使用模块：jieba, os, csv, re, time

| 模块  | 功能           |
| ----- | -------------- |
| csv   | csv文件的读写  |
| re    | 正则表达式匹配 |
| jieba | 分词           |

```python
__init__(self, filename, keys, name, sex, age, school, city, height, weight)
	MyBot的初始化操作，初始化机器人信息，并导入数据表
		filename QA数据库路径，keys api_keys, else 机器人的身份信息
		return None

update_bot_info(self)	-> None
	更新机器人的身份信息的QA库
    	return None
    
ask(self, sentence)	-> str
	查找答案，并返回答案或无答案时的回答（无法理解 或 找不到）
		sentence 询问的问题
		return 答案

find(self, sentence)	-> str or int(0, 1)
	查找答案，先后查找：空语句; help;@开头的工具使用; QA库查找; 分词估计搜索.若找不到答案，则返回int值
    	sentence 询问的问题
   		return 答案

compare(self, sentence)	-> str or False
	通过jieba分词找出与近义词库进行替换的所有文本，再用文本相似度算法实现身份信息库和QA库的QA查找
	    sentence 询问的问题
   		return 答案

cut(sentence)	-> list of str
	jieba分词
    	sentence 输入句子
        return 分词列表
learn(self, filename)	-> bool
	通过正则表达式判断和文件OI以及csv文件写入，一次获取每个人同时发的多条语句，并实现QQ聊天记录的QA库生成
    filename 读入文件
    return 是否导入成功

__get_sentence(self, file)	-> str or False
	获取一条聊天记录的内容
		file 聊天记录文件名
    	return 句子

add_all(self, knowledge)	-> bool
	将一个追加的QA库加入self.database中
	    knowledge 追加的QA库
    	return 是否追加成功

add_one(self, new)	-> bool
	将单条语句加入self.database中
		new 新的[Q,A]
        return 是否追加成功

delete(self, index)	-> list of str or False
	将self.database中下标为index的条目删除并返回
    	index 要删除的那条QA的下标
    	return 删除的那条QA
    
update(self, index, new)	-> bool
	将下标为index的那条语句的条目更新为新的一条QA
	index 要更新的那条QA的下标, new 新的一条QA
    return 是否更新成功

update_to_file(self)	-> bool
	将self.database更新到文件中
	return 是否更新成功
```

## File similarity.py
### class Similarity

文本相似度算法：最小编辑距离，余弦相似度，语义相似度

使用模块：jieba

| 模块  | 功能 |
| ----- | ---- |
| jieba | 分词 |

```python
get_distance(sen1, sen2)	-> int
	最小编辑距离算法
    	sen1 句子1, sen2 句子2
    	return 最小编辑距离
    
get_vector(mList, totalSet)	-> list
	获取单个句子的向量列表
		mList 句子的分词列表, totalSet list1和list2合并后的列表转换后的集合
		return 单个句子的向量列表

get_cos_similarity(text1, text2)	-> float
	余弦相似度算法
    	text1 文本1, text2 文本2
		return 相似度

get_synonyms_similarity(sen1, sen2)	-> float
	语义相似度算法
    	text1 文本1, text2 文本2
		return 相似度
```
## File synonym.py
### class synonym

文本相似度算法：最小编辑距离，余弦相似度，语义相似度

使用模块：jieba

| 模块 | 功能        |
| ---- | ----------- |
| csv  | csv文件读写 |

```python
add(new)	-> bool
	添加一条近义词列表到self.synonyms_list中
    	new 新的近义词列表
    	return 是否添加成功
    
delete(index)	-> bool
	删除一条近义词列表
		删除self.synonyms_list中下标为index的近义词列表
		return 是否删除成功

update(index, new)	-> bool
	更新self.synonyms_list中下标为index的近义词列表为new这个列表
    	index 要更新的项的下标, new为新的近义词列表
		return 是否更新成功

get(word)	-> list of str
	获取word在近义词表中找到的所有近义词及本身构成的列表
    	word 寻找的词
		return 返回word在近义词表中找到的所有近义词及本身构成的列表
    
replace(word, sentence)	   -> list of str
	获取word的近义词及word本身替换word后得到的所有句子
    	word 判断近义词的词, sentence 句子
        return 所有近义词替换后的列表及原本句子

update_to_file(...)    -> bool
	将self.synonyms_list写入csv文件中
    	return 是否写入成功
    
__del__(...)	-> bool
	析构函数，对象销毁时自动执行update_to_file()方法



```


## File main.py

程序入口