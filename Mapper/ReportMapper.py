import csv
import os

from DAO.ReportDAO import ReportDAO
from Utils.SymbolHandler import ReportEnum


class ReportMapper(object):
    def __init__(self):
        self.__curpath = os.path.dirname(os.path.realpath(__file__))

        pass

    def __insert_header(self, report_file_path):
        '''
        清空csv文件的内容，并插入文件头
        '''
        with open(report_file_path, 'w', encoding='utf-8', newline='') as report_file:
            csv_writer = csv.writer(report_file)
            csv_writer.writerow([ReportEnum.REPORT_ID,  ReportEnum.DEFECT_EXPLANATION, \
                                 ReportEnum.DEFECT_REPRODUCTION_STEP, ReportEnum.DefectPictureEnum.IMG_URL])

    def insert(self, report):
        '''
        该方法能根据传入的report所属的task_id将其存入不同的文件
        :param report:
        :return:
        '''
        reportDAO = ReportDAO.createReportDAO(report)

        task_id = reportDAO.task_id
        report_file_path = './Data/Reports/task' + str(task_id) + '-reports' + '.csv'


        if not os.path.exists(report_file_path):
            self.__insert_header(report_file_path)

        # 不管扩增和评估
        with open(report_file_path, 'a', encoding='utf-8', newline='') as report_file:
            csv_writer = csv.writer(report_file)
            csv_writer.writerow([reportDAO.report_id, reportDAO.defect_explanation, \
                                 reportDAO.defect_reproduction_step, reportDAO.img_url])
