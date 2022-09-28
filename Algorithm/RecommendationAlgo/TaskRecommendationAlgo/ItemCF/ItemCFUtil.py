import math
from operator import itemgetter
from collections import defaultdict
from Utils import modelManager
from Utils.DataManager import *
import os


class ItemCFUtil(object):
    """ Item based Collaborative Filtering SimilarityAlgo Implementation"""

    def __init__(self, trainData, similarity="cosine", norm=True):
        self._trainData = trainData
        self._similarity = similarity
        self._isNorm = norm
        self._itemSimMatrix = dict()  # 物品相似度矩阵

    def similarity(self):
        N = defaultdict(int)  # 记录每个物品的喜爱人数
        for user, items in self._trainData.items():
            for i in items:
                self._itemSimMatrix.setdefault(i, dict())
                N[i] += 1
                for j in items:
                    if i == j:
                        continue
                    self._itemSimMatrix[i].setdefault(j, 0)
                    if self._similarity == "cosine":
                        self._itemSimMatrix[i][j] += 1
                    elif self._similarity == "iuf":
                        self._itemSimMatrix[i][j] += 1. / math.log1p(len(items) * 1.)

        # print(self._itemSimMatrix)
        for i, related_items in self._itemSimMatrix.items():
            for j, cij in related_items.items():
                self._itemSimMatrix[i][j] = cij / math.sqrt(N[i] * N[j])
        # 是否要标准化物品相似度矩阵
        if self._isNorm:
            for i, relations in self._itemSimMatrix.items():
                if len(relations) == 0:
                    continue
                else:
                    max_num = relations[max(relations, key=relations.get)]
                    # 对字典进行归一化操作之后返回新的字典
                    self._itemSimMatrix[i] = {k: v / max_num for k, v in relations.items()}

    '''
    return: {3: 2.34, 5:423342, 9:0.32}
    '''

    def recommend(self, user, N, K):
        """
        :param user: 被推荐的用户user
        :param N: 推荐的商品个数
        :param K: 查找的最相似的用户个数
        :return: 按照user对推荐物品的感兴趣程度排序的N个商品
        """
        recommends = dict()
        # 先获取user的喜爱物品列表
        items = self._trainData[user]

        for item in items:
            a = self._itemSimMatrix[item].items()
            # 对每个用户喜爱物品在物品相似矩阵中找到与其最相似的K个
            for i, sim in sorted(self._itemSimMatrix[item].items(), key=itemgetter(1), reverse=True)[:K]:
                if i in items:
                    continue  # 如果与user喜爱的物品重复了，则直接跳过
                recommends.setdefault(i, 0.)
                recommends[i] += sim
        # 根据被推荐物品的相似度逆序排列，然后推荐前N个物品给到用户
        return dict(sorted(recommends.items(), key=itemgetter(1), reverse=True)[:N])

    def train(self):
        trainModelPath = TrainModelManager.getTrainModelPath()
        try:
            print("start load item similarity matrix")
            self._itemSimMatrix = modelManager.load(trainModelPath)[0]
        except BaseException as e:
            print("Exception occurs: " + str(e))
            print("load item similarity matrix failed, start train...")
            self.similarity()
            # save user similarity matrix
            modelManager.save(trainModelPath, self._itemSimMatrix)

        print("train ended...")
        print("clean trainModel..." + trainModelPath)
        TrainModelManager.cleanTrainModel()
