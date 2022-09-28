import csv
import os

from DAO.ReportVecDAO import ReportVecDAO
from Utils.SymbolHandler import ReportVecEnum


class ReportVecMapper(object):

    def __insert_header(self,report_vec_file_path ):
        '''
        插入矩阵头: report_id,x,y
        :param report_vec_file_path:
        :return:
        '''
        with open(report_vec_file_path, 'w', encoding='utf-8', newline='') as report_vec_file:
            csv_writer = csv.writer(report_vec_file)
            csv_writer.writerow([ReportVecEnum.REPORT_ID,  ReportVecEnum.X, \
                                 ReportVecEnum.Y])

    def insert_report_vec(self, report_id, report_vec, report_vec_file_path):
        '''

        :param report_id:
        :param report_vec: 二维的nd array
        :param report_vec_file_path:
        :return:
        '''
        reportVecDAO = ReportVecDAO(report_id,report_vec)

        if not os.path.exists(report_vec_file_path):
            self.__insert_header(report_vec_file_path)

        with open(report_vec_file_path, 'a', encoding='utf-8', newline='') as report_vec_file:
            csv_writer = csv.writer(report_vec_file)
            csv_writer.writerow([reportVecDAO.report_id,reportVecDAO.X, reportVecDAO.Y])
            print("将报告{}存入{}, x = {}, y = {}".format(report_id, report_vec_file_path, reportVecDAO.X, reportVecDAO.Y) )

