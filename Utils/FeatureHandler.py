from Algorithm.SimilarityAlgo.PlainTextSimilarity import TF_IDF
from Utils.DataManager import *
from enum import Enum

from VO.Document import Document


class FeatureHandler(object):

    EMPHASIZED_USER_FEATURES = "emphasized_user_features"
    DESALTED_USER_FEATURES = "desalted_user_features"
    EMPHASIZED_TASK_FEATURES = "emphasized_task_features"
    DESALTED_TASK_FEATURES = "desalted_task_features"
    @staticmethod
    def getUserFeatures(row):
        proficiency = float(row[USER_PROFICIENCY])
        preference = str(row[USER_PREFERENCE])
        activity = float(row[USER_ACTIVITY])
        testDevices = str(row[USER_TEST_DEVICES])
        return { USER_PROFICIENCY: proficiency, USER_PREFERENCE: preference, USER_ACTIVITY: activity,  USER_TEST_DEVICES: testDevices }

    @staticmethod
    def getTaskFeatures(row):
        # TASK_TYPE,TASK_INTRODUCTION, WORKER_NUM_TOTAL, WORKER_NUM_LEFT, TASK_DIFFICULTY, TASK_REQUIRED_TEST_DEVICES
        taskType = str(row[TASK_TYPE])
        taskIntroduction = int(row[TASK_INTRODUCTION])
        workerNumTotal = int(row[WORKER_NUM_TOTAL])
        workerNumLeft = int(row[WORKER_NUM_LEFT])
        taskDifficulty = float(row[TASK_DIFFICULTY])
        taskRequiredTestDevices = str(row[TASK_REQUIRED_TEST_DEVICES])
        return { TASK_TYPE: taskType, TASK_INTRODUCTION: taskIntroduction, workerNumTotal: WORKER_NUM_TOTAL, workerNumLeft: WORKER_NUM_LEFT,\
                 TASK_DIFFICULTY: taskDifficulty, TASK_REQUIRED_TEST_DEVICES: taskRequiredTestDevices}

    @staticmethod
    def getRecommendationRules():
        pass


    @staticmethod
    def taskIsLikedAccordingToRules(userFeatures, taskFeatures, recommendationRules):
        emphasizedUserFeatures = recommendationRules.get(FeatureHandler.EMPHASIZED_USER_FEATURES, [])
        desaltedUserFeatures = recommendationRules.get(FeatureHandler.DESALTED_USER_FEATURES, [])
        emphasizedTaskFeatures = recommendationRules.get(FeatureHandler.EMPHASIZED_TASK_FEATURES, [])
        desaltedTaskFeatures = recommendationRules.get(FeatureHandler.DESALTED_TASK_FEATURES, [])


        # 构造特征矩阵
        featureMatrixBuilder = FeatureMatrixBuilder( userFeatures, taskFeatures )
        featureMatrixBuilder.buildProficiency()
        featureMatrixBuilder.buildPreference()
        featureMatrixBuilder.buildDeviceCompatibility()
        featureMatrix = featureMatrixBuilder.getFeatureMatrix()

        # 根据规则修改特征矩阵
        featureMatrix.setFeatureRules(emphasizedUserFeatures,desaltedUserFeatures, emphasizedTaskFeatures, desaltedTaskFeatures)
        featureMatrix.modifyAccordingToRules()
        likeDegree = featureMatrix.computeLikeDegree()

        return featureMatrix.isLiked(likeDegree, 0.0001)











    '''
    对特征根据推荐规则进行权重处理
    feature_dic: 输入的原始特征， 是一个字典， 形如{ "professioncy": 0.9, "preferrence": 0.8 }, 字典的value以及经过归一化
    @Return 经过权重处理的特征字典
    '''
    def modifyFeaturesByRules(self, feature_dict, emphasized_feature_list, desalted_features_list):
        self.preprocess(feature_dict)
        self.__emphasizeFeaturesByRules(feature_dict, emphasized_feature_list)
        self.__desaltFeaturesByRules(feature_dict, desalted_features_list)
        return feature_dict




class FeatureMatrix(object):
    PROFICIENCY = "proficiency"
    PREFERENCE = "preference"
    DEVICE_COMPATIBILITY = "test_device_compatibility"

    class FilteredUserFeatureEnum(Enum):
        USER_PROFICIENCY
        USER_PREFERENCE
        USER_TEST_DEVICES

    class FilteredTaskFeatureEnum(Enum):
        TASK_TYPE
        TASK_DIFFICULTY
        TASK_REQUIRED_TEST_DEVICES


    def __init__(self, proficiency, preference, deviceCompatibility):
        self.__matrix = {
            FeatureMatrix.PROFICIENCY: proficiency,
            FeatureMatrix.PREFERENCE: preference,
            FeatureMatrix.DEVICE_COMPATIBILITY: deviceCompatibility
        }
        self.__emphasizedFeatures = set()
        self.__desaltedFeatures = set()


    def setFeatureKV(self, KEY, VALUE):

        if KEY in self.__matrix.keys():
            self.__matrix[KEY] = VALUE

    '''
    根据用户设定的特征修改规则，设定特征矩阵的修改规则
    emphasizedUserFeatures: ["ce", "fwef"]
    '''
    def setFeatureRules(self, emphasizedUserFeatures, desaltedUserFeatures,emphasizedTaskFeatures,desaltedTaskFeatures ):

        if USER_PROFICIENCY in emphasizedUserFeatures or TASK_DIFFICULTY in emphasizedTaskFeatures:
            self.__emphasizedFeatures.add( FeatureMatrix.PROFICIENCY )
        elif USER_PROFICIENCY in desaltedUserFeatures or TASK_DIFFICULTY in desaltedTaskFeatures:
            self.__desaltedFeatures.add(FeatureMatrix.PROFICIENCY)
        else:
            pass

        if USER_PREFERENCE in emphasizedUserFeatures or TASK_TYPE in emphasizedTaskFeatures:
            self.__emphasizedFeatures.add( FeatureMatrix.PREFERENCE )

        elif USER_PREFERENCE in desaltedUserFeatures or TASK_TYPE in desaltedTaskFeatures:
            self.__desaltedFeatures.add(FeatureMatrix.PREFERENCE)
        else:
            pass

        if USER_TEST_DEVICES in emphasizedUserFeatures or TASK_REQUIRED_TEST_DEVICES in emphasizedTaskFeatures:
            self.__emphasizedFeatures.add(FeatureMatrix.DEVICE_COMPATIBILITY)
        elif USER_TEST_DEVICES in desaltedUserFeatures or TASK_REQUIRED_TEST_DEVICES in desaltedTaskFeatures:
            self.__desaltedFeatures.add(FeatureMatrix.DEVICE_COMPATIBILITY)
        else:
            pass
        return

        # for userK, userV in emphasizedUserFeatures:
        #     if userK ==  in emphasizedTaskFeatures:
        #         self.__emphasizedFeatures.add(userK)
        #
        # for userK, userV in desaltedUserFeatures:
        #     if userK in desaltedTaskFeatures:
        #         self.__desaltedFeatures.add( userK )
        pass

    '''
    根据特征矩阵的修改规则, 对特征矩阵进行修改
    '''
    def modifyAccordingToRules(self):
        for k,v in self.__matrix.items():
            if k in self.__emphasizedFeatures:
                v *= 2
            elif k in self.__desaltedFeatures:
                v /= 2
            else:
                pass

    '''
    根据特征矩阵， 计算出该用户 - 任务 对的亲和程度
    '''
    def computeLikeDegree(self):
        likeDegree = float()
        for k, v in self.__matrix.items():
            likeDegree += v
        return likeDegree

    '''
    根据亲和程度，判断用户是否喜欢该任务
    '''
    def isLiked(self, likeDegree,likeThreshold = 0.01):
        return likeDegree >= likeThreshold


'''
   input: userFeatures, taskFeatures， 只采用一部分特征来构建特征矩阵
   { USER_PROFICIENCY: 0.432,  USER_PREFERENCE: "performance test" , USER_TEST_DEVICES： "iOS, Android" }
   和
   { TASK_DIFFICULTY： 0.645，TASK_TYPE："function test" ， TASK_REQUIRED_TEST_DEVICES："Linux, "Windows"   }


   output: 对应于上面三维的 3 * 1特征矩阵， 每个元素都是一个权重
   {
       USER_PROFICIENCY: 0.432,
       USER_PREFERENCE: 0.443,
       USER_TEST_DEVICES: 0.431
   }
   '''
class FeatureMatrixBuilder(object):

    def __init__(self, userFeatures, taskFeatures):
        self.__userFeatures = userFeatures
        self.__taskFeatures = taskFeatures

        self.__proficiency = 0.0
        self.__preference = ""
        self.__deviceCompatibility = 0.0

    def buildProficiency(self):
        proficiencyValue = 1 - abs( self.__userFeatures.get(USER_PROFICIENCY, 0.0)  - self.__taskFeatures.get(TASK_DIFFICULTY, 0.0) )

        pass
    def buildPreference(self):
        plainTextSimilarityStrategy = TF_IDF()

        preference = plainTextSimilarityStrategy.computeTextSimilarity(
            Document(1, self.__userFeatures.get(USER_PREFERENCE)), \
            Document(2, self.__taskFeatures.get(TASK_TYPE)))
        self.__preference = preference

    def buildDeviceCompatibility(self):
        plainTextSimilarityStrategy = TF_IDF()

        deviceCompatibility = plainTextSimilarityStrategy.computeTextSimilarity(
            Document(1, self.__userFeatures.get(USER_TEST_DEVICES)), \
            Document(2, self.__taskFeatures.get(TASK_REQUIRED_TEST_DEVICES)))
        self.__deviceCompatibility = deviceCompatibility



    def getFeatureMatrix(self):
        return FeatureMatrix(  self.__proficiency, self.__preference, self.__deviceCompatibility )



class RawUserFeature:
    USER_PROFICIENCY = 'proficiency'
    USER_PREFERENCE = 'preference'
    USER_ACTIVITY = 'activity'
    USER_TEST_DEVICES = 'test_devices'

class RawTaskFeature:
    TASK_TYPE = 'task_type'
    TASK_INTRODUCTION = 'task_introduction'
    WORKER_NUM_TOTAL = 'worker_num_total'
    WORKER_NUM_LEFT = 'worker_num_left'
    TASK_DIFFICULTY = 'task_difficulty'
    TASK_REQUIRED_TEST_DEVICES = 'required_test_devices'


