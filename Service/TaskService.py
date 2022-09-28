from Algorithm.RecommendationAlgo.TaskRecommendationAlgo.ItemCF.ItemCF import ItemCF
from Utils.FeatureHandler import *
from Utils.DataManager import *

from Utils.SymbolHandler import UserEnum
from Utils.SymbolHandler import AlgorithmEnum


class TaskService(object):

    def __init__(self):  # 数据源， 用于给模型训练提供数据
        self.__featureHandler = FeatureHandler()
        self.__mock_recommended_tasks = [{"task_id": 27, "recommendation_degree": 0.9872},
                                         {"task_id": 29, "recommendation_degree": 0.6252}]

        return

    # 将所有数据存入数据源
    def __saveIntoDataSource(self, *users):
        for user in users:
            rows = DataSourceManager.rowMapper(user)
            for row in rows:
                DataSourceManager.saveOneRow(row)
        return

    def __cleanDataSource(self):
        DataSourceManager.cleanDataSource()

    def saveTaskRecommendationData(self, prepareTaskRecommendationTrainingDataDTO):
        userList = prepareTaskRecommendationTrainingDataDTO.userList
        self.__saveIntoDataSource(*userList)

    def get_top_n_recommended_tasks(self, getRecommendedTasksDTO):
        user = getRecommendedTasksDTO.user
        recommendation_rules = getRecommendedTasksDTO.recommendation_rules
        recommended_task_num = getRecommendedTasksDTO.recommended_task_num
        algorithm = getRecommendedTasksDTO.algorithm
        recommendation_threshold = getRecommendedTasksDTO.recommendation_threshold

        result_list = list()

        self.__saveIntoDataSource(user)  # 将该用户的记录也存入数据源
        user_id = user.get(UserEnum.USER_ID)

        if algorithm == AlgorithmEnum.RecommendationAlgoEnum.TaskRecommendationAlgoEnum.ITEM_CF:
            taskRecommendationStrategy = ItemCF()
        else:  # todo
            taskRecommendationStrategy = ItemCF()

        result_list = taskRecommendationStrategy.get_top_n_recommended_tasks(user_id, recommendation_rules,
                                                                            recommended_task_num,
                                                                            recommendation_threshold)
        return result_list

    def mock_get_top_n_recommended_task_ids(self, user, recommendationRules, recommendedTaskNum, algorithm,
                                            recommendation_threshold):

        return self.__mock_recommended_tasks

    def mock_cluster_reports(self):
        return \
            '''
        {
    {
        "reportId": 10,
        "coordinate": [0.23, 0.87],
        "clusterId": 19
    },
    {
        "reportId": 86,
        "coordinate": [0.299, 0.882],
        "clusterId": 325
    },
    {
        "reportId": 19,
        "coordinate": [0.293, 0.9887],
        "clusterId": 923
    },
    {
        "reportId": 31,
        "coordinate": [0.003, 0.037],
        "clusterId": 324
    }
}
        '''
