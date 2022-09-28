from Algorithm.SimilarityAlgo.ReportSimilarityStrategy import ReportSimilarityStrategy
from Mapper.ReportSimilarityMatrixMapper import *


class DeepSimilarity(ReportSimilarityStrategy):

    '''
    index,-1,11,14,15
    -1,1.0,0.7151,0.6004,0.75
    11,0.7151,1.0,0.5001,0.5001
    14,0.6004,0.5001,1.0,0.5001
    15,0.75,0.5001,0.5001,1.0
    '''
    def get_similar_reports(self, report_id, report_sim_matrix_file_path):
        '''

        :param report_id: 待被比较的report的id
        :param report_sim_matrix_file_path:
        :return: { [report_id]: [similarity], ... }, 按相似度降序排列
        '''
        report_mapper = ReportSimilarityMatrixMapper()
        report_id_dict = report_mapper.get_row(report_id, report_sim_matrix_file_path)

        sorted_report_id_similarity_kv_list = sorted(report_id_dict.items(), key = lambda kv:(kv[1], kv[0]), reverse=True)

        res_dict = dict( sorted_report_id_similarity_kv_list )
        res_dict.pop(report_id) # 去除要被比较的报告

        return res_dict

if __name__ == "__main__":
    deepSim = DeepSimilarity()
    res_dict = deepSim.get_similar_reports(14, '/Users/lyk/Projects/Volatile/ai-volatile/Data/ReportSimMatrices/task1-report-sim-matrix.csv')
    print(res_dict)
    # print( {1: 2} )