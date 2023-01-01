import requests
from Utils.requestData import *

json_data = {'a': 1, 'b': 2}


def doPost(json_data):
    r = requests.post("http://127.0.0.1:5001/add", json=json_data)
    print(r.headers)
    print(r.text)
    return


def testPostGetRecommendedTasks():
    data = PostGetRecommendedTasksData

    r = requests.post("http://127.0.0.1:5001/getRecommendedTasks", json=data)
    print(r.headers)
    print(r.text)


def testPostPrepareTaskRecommendationTrainingData():
    data = PostPrepareTaskRecommendationTrainingData
    r = requests.post("http://127.0.0.1:5001/prepareTaskRecommendationTrainingData", json=data)
    print(r.headers)
    print(r.text)


def testPrepareReportTrainingData():
    data = PostPrepareReportSimilarityTrainingData_XinQuBuLuo2
    r = requests.post("http://127.0.0.1:5001/prepareReportTrainingData", json=data)
    print(r.headers)
    print(r.text)


def testGetSimilarReports():
    data = PostGetSimilarReportsData_Report309
    r = requests.post("http://127.0.0.1:5001/getSimilarReports", json=data)
    print(r.headers)
    print(r.text)

def testGetRecommendedReports():
    data = PostGetRecommendedReportsData
    r = requests.post("http://127.0.0.1:5001/getRecommendedReports", json=data)
    print(r.headers)
    print(r.text)

def testClusterReports():
    data = PostClusterReportsData
    r = requests.post("http://127.0.0.1:5001/clusterReports",json=data)
    print(r.headers)
    print(r.text)

def testGetAugmentedReports():
    data = PostGetAugmentedReportsData
    r = requests.post("http://127.0.0.1:5001/getAugmentedReports",json=data)
    print(r.headers)
    print(r.text)

def testGetReportEvaluation():
    data = PostGetReportEvaluationData
    r = requests.post("http://127.0.0.1:5001/getReportEvaluation", json=data)
    print(r.headers)
    print(r.text)


if __name__ == "__main__":

    # testPostPrepareTaskRecommendationTrainingData()
    # testPostGetRecommendedTasks()

    # task_id = 2
    # testPrepareReportTrainingData()
    # testGetSimilarReports()
    # testGetRecommendedReports()
    testClusterReports()
    # testGetReportEvaluation()# 自动化评估
    # testGetAugmentedReports()
