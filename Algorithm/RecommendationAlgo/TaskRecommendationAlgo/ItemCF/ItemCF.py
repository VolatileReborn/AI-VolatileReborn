from Algorithm.RecommendationAlgo.TaskRecommendationAlgo.TaskRecommendationStrategy import TaskRecommendationStrategy
from Utils import movielens_loader
from Utils.DataManager import *
from Algorithm.RecommendationAlgo.TaskRecommendationAlgo.\
    ItemCF.ItemCFUtil import ItemCFUtil
from Utils.SymbolHandler import TaskEnum
import abc



class ItemCF( TaskRecommendationStrategy ):
    '''
        return：
            {
            [3,0.432], [4,0.3221], [35,0.321]
            }
    '''

    def get_top_n_recommended_tasks(self, UserIdToBeRecommended, recommendationRules=[], recommendedTaskNum=5, recommendationThreshold=0.5):
        ####################################################################################
        # ItemCF 基于物品的协同过滤算法
        ####################################################################################

        dataSourcePath = DataSourceManager.getDataSourcePath()

        '''
        train: 已有的矩阵， test： 要被推荐用户的向量
        test: 被推荐的user的user-item矩阵， 因为只推荐一个user， 所以它只有一行
        '''
        train, test = movielens_loader.LoadMovieLensData(dataSourcePath, 0.8, UserIdToBeRecommended,
                                                         recommendationRules)

        resultDict = dict()
        print("train data size: %d, test data size: %d" % (len(train), len(test)))
        ItemCF = ItemCFUtil(train, similarity='iuf', norm=True)
        ItemCF.train()

        print("start recommend ...")

        assert len(test.keys()) == 1

        # 只返回一个dict
        for user in test.keys():  # 这里实际上只有一个key
            try:
                resultDict = ItemCF.recommend(user, recommendedTaskNum,
                                              80)  # 对每个用户，从与其喜爱的任务相似的80个任务中推荐 recommendedTaskNum 个任务
            except KeyError:
                resultDict = ItemCF.recommend(user, recommendedTaskNum, 80)  # 再推荐一次
            print(resultDict)

        # 将dict包装成返回的list
        resultList = list()
        resultList = self.__wrapDictToList(resultDict)
        resultList = self.__filtResultList(resultList)
        return resultList

        ############################# Toy Example ##############################
        # train = dict({'A':['a','b','d'], 'B':['b','c','e'], 'C':['c','d'], 'D':['b','c','d'], 'E':['a','d']})
        # test = dict({'C':['a']})
        # ItemCF = itemcf.ItemCF(train, similarity='iuf', norm=True)
        # ItemCF.train()
        #
        # print(ItemCF.recommend('C', 5, 80))
    '''
    resultDict: {1:0.4332, 2: 0.41312, 24:0.23342}
    resultLIst: [ {"task_id": 1, "recommendation_degree": 0.4332 }, {...}... ]
    '''
    def __wrapDictToList(self, resultDict):
        resultList = []
        for taskId, recommendationDegree in resultDict.items():
            task_id = taskId
            recommendation_degree = recommendationDegree

            item = { TaskEnum.TASK_ID: task_id, TaskRecommendationStrategy.RECOMMENDATION_DEGREE: recommendation_degree }
            resultList.append(item)
        return resultList

    '''
    对返回对推荐报告进行过滤， 目前只是过滤掉推荐程度低于0的任务
    '''
    def __filtResultList(self , originalList ):
        resultList = list()
        for item in originalList:
            if item.get(TaskRecommendationStrategy.RECOMMENDATION_DEGREE) <= 0:
                continue
            else:
                resultList.append(item)
        return resultList


if __name__ == "__main__":
    ItemCF()
