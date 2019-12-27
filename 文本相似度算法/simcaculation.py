import distance
import jieba
import synonyms
import math
#返回分词后文本对应的一个向量
def getVector(mList, totalSet):
    mSet = set(mList)       ##set为集合，不存在重复元素
    mDict = dict()
    for word in totalSet:   ##初始化
        mDict[word] = 0
    for word in mList:      ##计数
        mDict[word] = mDict[word] + 1
    return [mDict[word] for word in mDict]      ##返回计数对应的向量

#返回余弦相似度值
def get_cosSimilarity(text1, text2):
    list1 = [i for i in jieba.cut(text1, cut_all=True) if i != '']      ##分词结果
    list2 = [i for i in jieba.cut(text2, cut_all=True) if i != '']
    totalSet = set(list1 + list2)       #返回list1和list2合并后的列表转换后的集合
    vector1 = getVector(list1, totalSet)
    vector2 = getVector(list2, totalSet)
    num1 = num2 = num3 = 0
    mLen = len(vector1)
    for i in range(mLen):
        num1 += vector1[i]*vector2[i]       #Ai*Bi
        num2 += vector1[i]**2               #Ai平方和
        num3 += vector2[i]**2               #Bi平方和
    return num1 / (math.sqrt(num2)*math.sqrt(num3))


fin = open('simcaculation.txt', 'r', encoding='UTF-8')      #打开文件
fout = open('result.txt', 'w', encoding='UTF-8')
while(True):                    #循环
    line = fin.readline()       #循环读入行
    if not line:                #文件结尾判断
        break
    texts = line.split()        #将一行按空格、回车等字符分开，texts[0]和texts[1]分别是两个文本字符串
    editDistance = distance.levenshtein(texts[0], texts[1])     #编辑距离相似度
    cosSimilarity = get_cosSimilarity(texts[0], texts[1])       #余弦相似度值
    synonymsSimilarity = synonyms.compare(texts[0], texts[1])   #语义相似度
    fout.write('{:s}\t{:s}\t{:d}\t{:.2f}\t{:.2f}\n'.format(texts[0],    #写入文件
                                                           texts[1], editDistance,cosSimilarity, synonymsSimilarity))
fin.close() #文件关闭
fout.close()
