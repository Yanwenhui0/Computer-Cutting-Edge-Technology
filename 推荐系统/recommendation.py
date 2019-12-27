critics={
'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,'Just My Luck': 3.0,
              'Superman Returns': 3.5, 'You, Me and Dupree': 2.5, 'The Night Listener': 3.0},
'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5, 'Just My Luck': 1.5,
                 'Superman Returns': 5.0, 'The Night Listener': 3.0,'You, Me and Dupree': 3.5},
'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0, 'Superman Returns': 3.5,
                     'The Night Listener': 4.0},
'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0, 'The Night Listener': 4.5,
                 'Superman Returns': 4.0,'You, Me and Dupree': 2.5},
'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,'Just My Luck': 2.0, 'Superman Returns': 3.0,
                 'The Night Listener': 3.0, 'You, Me and Dupree': 2.0},
'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0, 'The Night Listener': 3.0,
                  'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},
'Toby': {'Snakes on a Plane':4.5,'You, Me and Dupree':1.0,'Superman Returns':4.0},
'Json': {'Lady in the Water': 1.0, 'Snakes on a Plane': 2.5,'Just My Luck': 4.5,
              'Superman Returns': 3},
'tom': {'Lady in the Water': 5.0, 'Just My Luck': 1.5, 'You, Me and Dupree': 3.0},
'penny': {'Snakes on a Plane': 5.0, 'Superman Returns': 3.5, 'The Night Listener': 4.0}}


# 返回person1 和 person2 欧式距离的倒数
def sim_distance(prefs,person1,person2):
  si={}
  for item in prefs[person1]:
    if item in prefs[person2]: si[item]=1
  # 如果没有看过共同的电影则返回0
  if len(si)==0: return 0
  # 欧式距离计算公式
  sum_of_squares=sum([pow(prefs[person1][item]-prefs[person2][item],2)
                      for item in prefs[person1] if item in prefs[person2]])
  return 1/(1+sum_of_squares)

def topMatches(prefs,person,n=3,similarity=sim_distance):
  scores=[(similarity(prefs,person,other),other)
                  for other in prefs if other!=person]
  scores.sort()
  scores.reverse()
  return scores[0:n]
#print(topMatches(critics,'Toby',n=3))

#得到最终推荐的电影
def getRecommendations(prefs, person, similarity=sim_distance):
    totals = {}
    simSums = {}
    top = topMatches(critics,'Toby',n=3)

    for other in prefs:
        if other == person: continue    # 不用和自己做对比
        sim = similarity(prefs, person, other) #计算other和person的相似度
        if sim <= 0: continue        # 去掉得分小于0的
        for item in prefs[other]:
            if item not in prefs[person] or prefs[person][item] == 0:             # 只推荐自己没有看过的
                # 计算相似度得分
                totals.setdefault(item, 0)
                totals[item] += prefs[other][item] * sim
                # Sum of similarities
                simSums.setdefault(item, 0)
                simSums[item] += sim
    #for i,j in totals.items():
        #print(simSums[i])
    rankings = [(total / simSums[item], item) for item, total in totals.items()]     # 电影得分列表
    rankings.sort()    # 对其进行排序
    rankings.reverse()
    return rankings



print(getRecommendations(critics,'Json',sim_distance))
print(getRecommendations(critics,'tom',sim_distance))
print(getRecommendations(critics,'penny',sim_distance))
