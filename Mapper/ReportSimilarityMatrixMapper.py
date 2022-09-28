import csv
from csv import DictReader

class ReportSimilarityMatrixMapper(object):

    @staticmethod
    def get_report_sim_matrix_file_path(task_id):
        report_sim_matrix_file_path = './Data/ReportSimMatrices/task' + str(task_id) + '-report-sim-matrix' + '.csv'
        return report_sim_matrix_file_path

    def get_row(self, report_id, report_sim_matrix_file_path):
        '''

        :param report_id:
        :param report_sim_matrix_file_path:
        :return: { [report_id]: [similarity], ... }, 不包含key为'index'和'-1',即返回的是所有真实报告的相似度, 注意report_id是int, similarity是float
        '''
        res_row_str = {}
        res_row_int = {}

        with open(report_sim_matrix_file_path, 'r', encoding='utf-8') as report_file:
            csv_dict_reader = DictReader(report_file)

            for row in csv_dict_reader:

                if row.get('index') == str(report_id):
                    row.pop('index')
                    row.pop('-1')
                    res_row_str = row
                    break
            if res_row_str == {}:
                print("Error: 矩阵行为空")
                return res_row_int
            else:
                for k,v in res_row_str.items():
                    k_int  = int(k)
                    res_row_int[ k_int ] = float(v)

        return res_row_int



if __name__ == "__main__":
    mapper = ReportSimilarityMatrixMapper()
    res_dict = mapper.get_row(14, '/Users/lyk/Projects/Volatile/ai-volatile/Data/ReportSimMatrices/task1-report-sim-matrix.csv')
    print(res_dict)


