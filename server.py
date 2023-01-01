# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import json

from flask import Flask, request, Response
from werkzeug.utils import secure_filename
import os

from DTO.GetAugmentedReportsDTO import GetAugmentedReportsDTO
from DTO.PrepareTaskRecommendationTrainingDataDTO import *
from DTO.PrepareReportTrainingDataDTO import *

from DTO.ClusterReportsDTO import *
from DTO.GetSimilarReportsDTO import *
from DTO.GetRecommendedReportsDTO import *

from DTO.GetRecommendedTasksDTO import *
from DTO.GetReportEvaluationDTO import *


from VO.ClusterReportsVO import *
from VO.GetSimilarReportsVO import *
from VO.GetRecommendedTasksVO import *

from Service.ReportService import *
from Service.TaskService import *
from Utils.SymbolHandler import *

from VO.Document import Document

# Flask初始化参数尽量使用你的包名，这个初始化方式是官方推荐的，官方解释：http://flask.pocoo.org/docs/0.12/api/#flask.Flask
# app = Flask(__name__, static_folder="./static", template_folder='./templates')
app = Flask(__name__)

# 禁止对中文进行转码
app.config['JSON_AS_ASCII'] = False

app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}  # 集合类型



def allowed_file(filename):  # 判断filename是否有后缀以及后缀是否在app.config['ALLOWED_EXTENSIONS']中
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


@app.route('/upload', methods=['POST'])
def upload():
    upload_file = request.files['image']  # 客户端上传的图片必须以image标识 ;; upload_file是上传文件对应的对象
    if upload_file and allowed_file(upload_file.filename):
        filename = secure_filename(upload_file.filename)
        # 将文件保存到 static/uploads 目录，文件名同上传时使用的文件名
        # app.root_path获取server.py所在目录在文件系统中的绝对路径
        # 用来将upload_file保存在服务器的文件系统中，参数最好是绝对路径
        # 函数os.path.join()用来将使用合适的路径分隔符将路径组合起来
        upload_file.save(os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], filename))
        return 'info is ' + request.form.get('info', '') + '. success'
    else:
        return 'failed'


@app.route('/api')
def hello_world():
    return "Hello World!"  # HTTP响应报文的实体部分


@app.route('/add', methods=['POST'])
def add():
    print(request.headers)
    print(type(request.json))  # 如果POST的数据是JSON格式, request.json会自动将json数据转换成Python类型（字典或者列表）
    print(request.json)
    result = {'sum': request.json['a'] + request.json['b']}
    resp = Response(json.dumps(result), mimetype='application/json')
    resp.headers.add('Server', 'python flask')
    return resp


@app.route('/getSimilarReports', methods=['POST'])
def getSimilarReports():
    # report = json_data.get(ReportEnum.REPORT, {})
    # relatedReports = json_data.get(ReportEnum.RELATED_REPORTS)

    # # 这里只采用defect_reproduction_step
    # uploadedReportText = report.get(ReportEnum.DEFECT_REPORDUCTION_STEP)
    # origin_report_id = report.get(ReportEnum.REPORT_ID)
    #
    # originalDocument = Document(origin_report_id, uploadedReportText)
    # comparedDocuments = list()
    #
    # for relatedReport in relatedReports:
    #     comparedDocuments.append( Document(relatedReport.get(ReportEnum.REPORT_ID), relatedReport.get(ReportEnum.DEFECT_REPORDUCTION_STEP)) )
    #
    # similarReportNum = json_data.get(SimilarityEnum.SIMILAR_REPORT_NUM, 3 ) # 默认为3
    # algorithm = json_data.get(SimilarityEnum.ALGORITHM, SimilarityAlgo.TF_IDF)
    #
    # top_n_similar_report_ids = reportService.get_top_n_plain_text_similar_reports(originalDocument,comparedDocuments,similarReportNum,algorithm)
    # print("########\nanswer: ")
    # print(top_n_similar_report_ids)
    # return Response( json.dumps(top_n_similar_report_ids), mimetype='application/json' )

    getSimilarReportsDTO = GetSimilarReportsDTO(request.json)

    reportService = ReportService()
    similarReportIdList = reportService.get_top_n_similar_reports(getSimilarReportsDTO)
    return Response(json.dumps(similarReportIdList), mimetype='application/json')

@app.route('/getRecommendedReports', methods=['POST'])
def getRecommendedReports():
    getSimilarReportsDTO = GetRecommendedReportsDTO(request.json)

    reportService = ReportService()
    similarReportIdList = reportService.get_top_n_recommended_reports(getSimilarReportsDTO)
    return Response(json.dumps(similarReportIdList), mimetype='application/json')


@app.route('/getRecommendedTasks', methods=['POST'])
def getRecommendedTasks():

    getRecommendedTasksDTO = GetRecommendedTasksDTO(request.json)

    task_service = TaskService()
    recommended_task_id_list = task_service.get_top_n_recommended_tasks(getRecommendedTasksDTO)
    return Response(json.dumps(recommended_task_id_list), mimetype='application/json')


@app.route('/prepareTaskRecommendationTrainingData', methods=['POST'])
def prepareTaskRecommendationTrainingData():
    prepareTaskRecommendationTrainingDataDTO = PrepareTaskRecommendationTrainingDataDTO(request.json)

    task_service = TaskService()
    task_service.saveTaskRecommendationData(prepareTaskRecommendationTrainingDataDTO)
    return Response(json.dumps("Task Data Prepared Successfully"), mimetype='application/json')


@app.route('/prepareReportTrainingData', methods=['POST'])
def prepareReportTrainingData():
    prepareReportTrainingDataDTO = PrepareReportTrainingDataDTO(request.json)

    report_service = ReportService()
    report_service.prepare_report_data(prepareReportTrainingDataDTO)
    return Response(json.dumps("Report Data Prepared Successfully"), mimetype='application/json')

@app.route('/getAugmentedReports', methods=['POST'])
def getAugmentedReports():
    getAugmentedReportsDTO = GetAugmentedReportsDTO(request.json)

    report_service = ReportService()
    getAugmentedReportsVO = report_service.get_augmented_reports(getAugmentedReportsDTO)
    return Response(json.dumps(getAugmentedReportsVO.get_value()), mimetype='application/json')

@app.route('/getReportEvaluation', methods=['POST'])
def getReportEvaluation():
    getReportEvaluationDTO = GetReportEvaluationDTO(request.json)

    report_service = ReportService()
    getReportEvaluationVO = report_service.get_report_evaluation(getReportEvaluationDTO)
    return Response(json.dumps(getReportEvaluationVO.get_value()), mimetype='application/json')


@app.route('/clusterReports', methods=['POST'])
def clusterReports():
    clusterReportsDTO = ClusterReportsDTO(request.json)
    report_service = ReportService()
    clusterReportsVO = report_service.cluster_reports(clusterReportsDTO)
    return Response(json.dumps(clusterReportsVO), mimetype='application/json')


if __name__ == "__main__":
    # 这种是不太推荐的启动方式，我这只是做演示用，官方启动方式参见：http://flask.pocoo.org/docs/0.12/quickstart/#a-minimal-application



    app.run(host='0.0.0.0', port=int("5001"), debug=True)  # 将debug设置为True的另一个好处是，程序启动后，会自动检测源码是否发生变化，若有变化则自动重启程序
    print("JSON ASCII: " + app.config['JSON_AS_ASCII'])
