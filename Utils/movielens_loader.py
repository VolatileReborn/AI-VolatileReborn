import random
import pandas as pd
from Utils.DataManager import *
from Utils.FeatureHandler import FeatureHandler
# todo
def LoadMovieLensData(filepath, train_rate, UserIdToBeRecommended, recommendationRules):
    # ratings = pd.read_table(filepath, sep="::", header=None, names=["UserID", "TaskID", "Rating", "TimeStamp"],\
    #                         engine='python')
    ratings = DataSourceManager.getTableFromDataSource()
    ratings = ratings[[ USER_ID, TASK_ID, USER_PROFICIENCY, USER_PREFERENCE,USER_ACTIVITY, USER_TEST_DEVICES,TASK_TYPE, \
                        TASK_INTRODUCTION,WORKER_NUM_TOTAL, WORKER_NUM_LEFT,TASK_DIFFICULTY,TASK_REQUIRED_TEST_DEVICES]]

    train = []
    # 测试集，即被推荐的users， 这里只推荐一个人
    test = []
    # random.seed(3)
    for idx, row in ratings.iterrows():
        userId = int(row[USER_ID])
        taskId = int(row[TASK_ID])
        userFeatures = FeatureHandler.getUserFeatures(row)
        taskFeatures = FeatureHandler.getTaskFeatures(row)
        taskIsLiked = FeatureHandler.taskIsLikedAccordingToRules(userFeatures, taskFeatures, recommendationRules)

        if not taskIsLiked:
            continue
        if userId != UserIdToBeRecommended:
            train.append([userId, taskId])
        else:
            train.append([userId, taskId])
            test.append([userId, taskId])
    return PreProcessData(train), PreProcessData(test)




def PreProcessData(originData):
    """
    建立User-Item表，结构如下：
        {"User1": {MovieID1, MoveID2, MoveID3,...}
         "User2": {MovieID12, MoveID5, MoveID8,...}
         ...
        }
    """
    trainData = dict()
    for user, item in originData:
        trainData.setdefault(user, set()) # movies是个set
        trainData[user].add(item)
    return trainData

