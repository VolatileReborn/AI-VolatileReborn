import os

from Algorithm.ClusterAlgo.KMeans import KMeansStrategy
from Algorithm.RecommendationAlgo.ReportRecommendationAlgo.DeepRecommendation.DeepRecommendation import \
    DeepRecommendation
from Algorithm.TrainingAlgo.ReportTrainingAlgo.DeepPrior.DeepPrior import DeepPrior
from Algorithm.SimilarityAlgo.DeepSimilarity.DeepSimilarity import DeepSimilarity
from DTO.GetSimilarReportsDTO import *

from Mapper.ReportMapper import *
from VO.GetSimilarReportsVO import GetSimilarReportsVO


class ReportService(object):
    def __init__(self):
        return

    @staticmethod
    def __get_report_file_path(task_id):
        report_file_path = './Data/Reports/task' + str(task_id) + '-reports' + '.csv'
        return report_file_path

    @staticmethod
    def __get_report_sim_matrix_file_path(task_id):
        report_sim_matrix_file_path = './Data/ReportSimMatrices/task' + str(task_id) + '-report-sim-matrix' + '.csv'
        return report_sim_matrix_file_path

    @staticmethod
    def __get_report_vec_file_path(task_id):
        report_vec_file_path = './Data/ReportVectors/task' + str(task_id) + '-report-vecs' + '.csv'
        return report_vec_file_path

    @staticmethod
    def __get_report_file_dir_path():
        report_file_dir_path = './Data/Reports/'
        return report_file_dir_path

    @staticmethod
    def __get_report_sim_matrices_file_dir_path():
        report_sim_matrices_file_dir_path = './Data/ReportSimMatrices'
        return report_sim_matrices_file_dir_path

    @staticmethod
    def __get_report_vec_file_dir_path():
        report_vec_file_dir_path = './Data/ReportVectors'
        return report_vec_file_dir_path

    mock_result = [{"report_id": 7, "similarity": 0.922}, {"report_id": 2, "similarity": 0.855},
                   {"report_id": 9, "similarity": 0.543}]

    def prepare_report_data(self, prepareReportTrainingDataDTO):
        '''
        准备好报告数据（先清空之间的报告数据和中间结果），并计算出中间结果
        :return:
        '''
        report_list = prepareReportTrainingDataDTO.report_list

        training_algorithm = prepareReportTrainingDataDTO.algorithm
        task_id = prepareReportTrainingDataDTO.task_id

        self.__clear_previous_report_data_of_task(task_id)
        self.__save_report_data(report_list)

        self.train_reports(training_algorithm, task_id)
        return

    def train_reports(self, training_algorithm, task_id):
        '''
        使用训练算法根据报告数据计算出中间结果， 中间结果是报告相似度矩阵以及报告的二维向量，都存入对应文件
        :param training_algorithm: 默认是DeepPrior
        :param task_id: 任务id，用于找到对应的报告数据
        :return:
        '''
        if training_algorithm == AlgorithmEnum.TrainingAlgoEnum.DEEP_PRIOR:
            report_training_strategy = DeepPrior()
        else:
            report_training_strategy = DeepPrior()

        report_file_path = self.__get_report_file_path(task_id)
        report_sim_matrix_file_path = self.__get_report_sim_matrix_file_path(task_id)
        report_vec_file_path = self.__get_report_vec_file_path(task_id)

        report_training_strategy.train_reports(report_file_path, task_id, report_sim_matrix_file_path, report_vec_file_path)

        return

    def get_top_n_similar_reports(self, getSimilarReportsDTO):
        '''
            得到相似报告，如果要被比较的报告不在相似度矩阵内，该方法会报错
        '''

        similarity_algorithm = getSimilarReportsDTO.algorithm
        if similarity_algorithm == AlgorithmEnum.SimilarityAlgoEnum.ReportSimilarityAlgorithm.DEEP_SIMILARITY:
            report_similarity_strategy = DeepSimilarity()
        else:
            report_similarity_strategy = DeepSimilarity()

        task_id = getSimilarReportsDTO.task_id
        report_sim_matrix_file_path = self.__get_report_sim_matrix_file_path(task_id)

        similar_report_dict = report_similarity_strategy.get_similar_reports(getSimilarReportsDTO.report_id,
                                                                             report_sim_matrix_file_path)
        similar_report_list = list(similar_report_dict.items())
        top_n_similar_report_list = similar_report_list[: getSimilarReportsDTO.similar_report_num]

        res_dict_list = GetSimilarReportsVO(top_n_similar_report_list).get_value()
        return res_dict_list

    def get_top_n_recommended_reports(self, getRecommendedReportsDTO):

        recommendation_algorithm = getRecommendedReportsDTO.algorithm

        if recommendation_algorithm == AlgorithmEnum.RecommendationAlgoEnum.ReportRecommendationAlgoEnum. \
                DEEP_RECOMMENDATION:
            report_recommendation_strategy = DeepRecommendation()
        else:
            report_recommendation_strategy = DeepRecommendation()

        task_id = getRecommendedReportsDTO.task_id
        report_sim_matrix_file_path = self.__get_report_sim_matrix_file_path(task_id)

        # DeepRecommendation没有用到report_id，该变量目前无用
        report_id = getRecommendedReportsDTO.report_id

        report_id_list = report_recommendation_strategy.get_recommended_reports(report_sim_matrix_file_path)

        return report_id_list[:getRecommendedReportsDTO.recommended_report_num]

    # def get_top_n_plain_text_similar_reports(self, originalDocument, comparedDocuments, N, algorithm):
    #     if algorithm == ReportSimilarityAlgorithm.TF_IDF:
    #         plainTextSimilarityStrategy = TF_IDF()
    #     else:  # todo
    #         plainTextSimilarityStrategy = TF_IDF()
    #     return plainTextSimilarityStrategy.get_top_n_similar_reports(originalDocument, comparedDocuments, N)

    '''
    queried_report： string
    compared_reports：list(string)
    '''

    # def get_top_n_similar_report_ids(self, queried_report, compared_reports, N, algorithm):
    #
    #     queried_report = [queried_report]
    #     # return get_top_n_similar_result_ids( queried_report, compared_reports, N, algorithm)
    #     if algorithm == 'CosineSimilarity':
    #         textSimilarityStratefy = CosineTextSemanticSimilarityStrategy(queried_report, compared_reports)
    #     elif algorithm == 'SemanticSearch':
    #         textSimilarityStratefy = SemanticSearchTextSemanticSimilarityStrategy(queried_report, compared_reports)
    #     else:
    #         textSimilarityStratefy = BM25TextSemanticSimilarityStrategy(queried_report, compared_reports)
    #
    #     return textSimilarityStratefy.get_top_n_semantically_similar_reports(N)

    def cluster_reports(self, clusterReportsDTO):

        task_id = clusterReportsDTO.task_id

        report_vec_file_path = self.__get_report_vec_file_path(task_id)
        cluster_strategy = KMeansStrategy()

        res_list = cluster_strategy.cluster(report_vec_file_path)

        return res_list

    def __save_report_data(self, report_list):
        '''
        清空原有的报告数据和中间结果，插入新的报告数据
        重新插入(覆盖原有数据）所有报告数据， 按所属任务存入不同文件: ./Data/Reports/task*-reports.csv
        :param report_list:
        :return:
        '''

        report_mapper = ReportMapper()
        for report in report_list:
            report_mapper.insert(report)

    def __clear_previous_report_data_of_task(self, task_id):
        '''
        清空该任务下原有的报告数据和中间结果，即：
        1. 报告数据
        2. 报告的相似度矩阵
        3. 报告的向量
        :return:
        '''
        self.__clear_file( self.__get_report_file_path(task_id) )
        self.__clear_file(self.__get_report_sim_matrix_file_path(task_id))
        self.__clear_file(self.__get_report_vec_file_path(task_id))

    def __clear_previous_report_data(self):
        '''
        清空所有任务的所有报告数据和中间结果，该方法暂时没用
        :return:
        '''
        self.__clear_previous_data_in_dir(self.__get_report_file_dir_path())
        self.__clear_previous_data_in_dir(self.__get_report_sim_matrices_file_dir_path())
        self.__clear_previous_data_in_dir(self.__get_report_vec_file_dir_path())

    def __clear_previous_data_in_dir(self, report_file_dir):
        del_list = os.listdir(report_file_dir)
        for f in del_list:
            report_file_path = os.path.join(report_file_dir, f)
            if os.path.isfile(report_file_path):
                os.remove(report_file_path)

    def __clear_file(self, file_path):
        if os.path.exists(file_path):
            os.remove(file_path)


if __name__ == "__main__":
    similar_report_dict = {15: 0.9001, 11: 0.5001}
    similar_report_list = list(similar_report_dict.items())
    top_n_similar_report_list = similar_report_list
    res_dict_list = GetSimilarReportsVO(top_n_similar_report_list).get_value()
    print(res_dict_list)
