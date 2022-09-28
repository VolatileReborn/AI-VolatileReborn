import os
import pandas as pd

USER_ID = 'user_id'
USER_PROFICIENCY = 'proficiency'
USER_PREFERENCE = 'preference'
USER_ACTIVITY = 'activity'
USER_TEST_DEVICES = 'test_devices'

TASK_ID = "task_id"
TASK_TYPE = 'task_type'
TASK_INTRODUCTION = 'task_introduction'
WORKER_NUM_TOTAL = 'worker_num_total'
WORKER_NUM_LEFT = 'worker_num_left'
TASK_DIFFICULTY = 'task_difficulty'
TASK_REQUIRED_TEST_DEVICES = 'required_test_devices'

RATING = 'Rating'
TIME_STAMP = 'TimeStamp'


# todo


class DataSourceManager(object):
    __TEST_RATINGS = '/../Data/testRatings.dat'
    __USER_FEATURES_TEST = '/../Data/userFeaturesTest.dat'
    __TEST_OUTPUT = '/../Data/testOutput.dat'
    __dataSourcePath =  os.path.join(os.path.dirname(__file__) + __TEST_OUTPUT)

    #分隔符
    SEPARATOR = "::"



    def __init__(self):
        return

    @staticmethod
    def saveOneRow( row ):
        with open(DataSourceManager.__dataSourcePath, mode='a') as f:
            f.write(row)
            f.write('\n')
        return

    @staticmethod
    def saveRows(rows):
        for row in rows:
            DataSourceManager.saveOneRow(row)


    @staticmethod
    def getTableFromDataSource():
        names = [USER_ID, TASK_ID, RATING, TIME_STAMP, \
                    USER_PROFICIENCY, USER_PREFERENCE,USER_ACTIVITY,USER_TEST_DEVICES, \
                    TASK_TYPE,TASK_INTRODUCTION,WORKER_NUM_TOTAL,WORKER_NUM_LEFT,TASK_DIFFICULTY,TASK_REQUIRED_TEST_DEVICES]
        # names = ["UserId", "TaskId", "Rating", "TimeStamp"]
        fullTable = pd.read_table(DataSourceManager.__dataSourcePath, sep="::", names=names, skiprows=1,engine='python')
        print("full table:")
        print(fullTable)

        return fullTable


    @staticmethod
    def cleanDataSource():
        pass

    @staticmethod
    def getDataSourcePath():
        return DataSourceManager.__dataSourcePath

    #
    '''
    将一个user映射为数据源文件中的若干行
    @user: 形如：
        {
        "user_id": 77,
        "user_features": {
                "proficiency": 0.65,
                "preference": [
                    "performance test",
                    "function test"
                ],
                "activity": 0.11,
                "test_devices": [
                    "Android",
                    "Windows",
                    "iOS"
                ]
        },
        "related_tasks": [
            {
                "task_id": 44,
                "task_features": {
                    "task_type": "performance test",
                    "task_introduction": "irurefadadadadassda non in amet",
                    "worker_num_left": 26,
                    "worker_num_total": 57,
                    "task_difficulty": 0.432377,
                    "required_test_devices": [
                        "Android",
                        "Linux",
                        "iOS"
                    ]
                }
            },
            {
                "task_id": 82,
                "task_features": {
                    "task_type": "performance test",
                    "task_introduction": "ex eiuaddasasdasadssmod exercitation cupidatat",
                    "worker_num_left": 0,
                    "worker_num_total": 25,
                    "task_difficulty": 0.61,
                    "required_test_devices": [
                        "Android"
                    ]
                }
            },
            {
                "task_id": 11,
                "task_features": {
                    "task_type": "function test",
                    "task_introduction": "suntfs似懂非懂上的",
                    "worker_num_left": 53,
                    "worker_num_total": 60,
                    "task_difficulty": 0.3237,
                    "required_test_devices": [
                        "Android",
                        "Linux",
                        "iOS"
                    ]
                }
            },
            {
                "task_id": 99,
                "task_features": {
                    "task_type": "function test",
                    "task_introduction": "adipisicing veniam",
                    "worker_num_left": 2,
                    "worker_num_total": 11,
                    "task_difficulty": 0.72,
                    "required_task_devices": [
                        "Android",
                        "iOS"
                    ]
                }
            }
        ]
    }
    '''
    @staticmethod
    def rowMapper(user):
        resultRows = []

        userId = user.get(USER_ID)
        userFeatures = user.get('user_features')
        relatedTasks = user.get('related_tasks')

        proficiency = userFeatures.get(USER_PROFICIENCY)
        preference = userFeatures.get(USER_PREFERENCE)
        activity = userFeatures.get(USER_ACTIVITY)
        testDevices = userFeatures.get(USER_TEST_DEVICES)

        for task in relatedTasks:
            taskId = task.get(TASK_ID)
            taskFeatures = task.get('task_features')
            taskType = taskFeatures.get(TASK_TYPE)
            taskIntroduction = len( taskFeatures.get(TASK_INTRODUCTION) ) # 只记录任务介绍的长度
            workerNumTotal = taskFeatures.get(WORKER_NUM_TOTAL)
            workerNumLeft = taskFeatures.get(WORKER_NUM_LEFT)
            taskDifficulty = taskFeatures.get(TASK_DIFFICULTY)
            requiredTestDevices = taskFeatures.get( TASK_REQUIRED_TEST_DEVICES )

            rating = 3 # rating暂时没用
            timeStamp = 978301968 # 暂时没用

            row = DataSourceManager.__mergeFieldToRow(userId, taskId, rating, timeStamp, proficiency, preference, activity, testDevices, \
                                                            taskType, taskIntroduction, workerNumTotal, workerNumLeft, taskDifficulty, requiredTestDevices)
            resultRows.append(row)
        return resultRows

    @staticmethod
    def __mergeFieldToRow(*fields):
        if len(fields) == 0:
            return ""

        resultRow = ""
        for field in fields:
            if isinstance(field, int) or isinstance(field, float):
                field = str(field)
            elif isinstance(field, list):
                field = DataSourceManager.__convertListToStr(field)
            elif not isinstance(field, str):
                print("ERROR")
                print( fields )
            else:
                pass
            resultRow = resultRow + field + DataSourceManager.SEPARATOR
        resultRow = resultRow[: len(resultRow) - len(DataSourceManager.SEPARATOR)]
        print( "merged row \n" + str(resultRow) )
        return resultRow


        # userId = user.get("user_id")
        # userFeatures = user.get("userFeatures")
        # relatedTaskList = user.get("related_tasks")
        #
        # for task in relatedTaskList:
        #     taskId = task.get("task_id")
        #     taskFeatures = task.get("task_features")
        #     return {}
    @staticmethod
    def __convertListToStr(strList):
        return ",".join(strList)



class TrainModelManager(object):
    __trainModelPath = os.path.join(os.path.dirname(__file__) + '/../TrainedModels/itemcf.pkl')

    @staticmethod
    def getTrainModelPath():
        return  TrainModelManager.__trainModelPath

    @staticmethod
    def cleanTrainModel():
        os.remove(TrainModelManager.__trainModelPath)

if __name__ == "__main__":
    with open(TrainModelManager.getTrainModelPath(), 'a') as f:
        f.write("afdafaa")