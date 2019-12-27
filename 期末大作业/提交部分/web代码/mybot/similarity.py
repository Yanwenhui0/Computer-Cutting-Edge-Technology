import distance
import jieba
import synonyms
import math


class Similarity:
    @staticmethod
    def get_distance(sen1, sen2):
        return distance.levenshtein(sen1, sen2)  # 编辑距离相似度

    # 返回分词后文本对应的一个向量
    @staticmethod
    def get_vector(mList, totalSet):
        mSet = set(mList)  #set为集合，不存在重复元素
        mDict = dict()
        for word in totalSet:  #初始化
            mDict[word] = 0
        for word in mList:  #计数
            mDict[word] = mDict[word] + 1
        return [mDict[word] for word in mDict]  #返回计数对应的向量

    # 返回余弦相似度值
    @staticmethod
    def get_cos_similarity(text1, text2):
        list1 = [i for i in jieba.cut(text1, cut_all=True) if i != '']  #分词结果
        list2 = [i for i in jieba.cut(text2, cut_all=True) if i != '']
        totalSet = set(list1 + list2)  # 返回list1和list2合并后的列表转换后的集合
        vector1 = Similarity.get_vector(list1, totalSet)
        vector2 = Similarity.get_vector(list2, totalSet)
        num1 = num2 = num3 = 0
        mLen = len(vector1)

        for i in range(mLen):
            num1 += vector1[i] * vector2[i]  # Ai*Bi
            num2 += vector1[i] ** 2  # Ai平方和
            num3 += vector2[i] ** 2  # Bi平方和
        if num2 == 0 or num3 == 0:
            return 0
        return num1 / (math.sqrt(num2) * math.sqrt(num3))

    @staticmethod
    def get_synonyms_similarity(sen1, sen2):
        return synonyms.compare(sen1, sen2)  # 语义相似度
