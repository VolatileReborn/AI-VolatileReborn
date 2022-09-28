from Utils.SymbolHandler import ReportEnum, AlgorithmEnum


class GetSimilarReportsDTO(object):
    def __init__(self, json_data):
        # 要被比较的报告的id
        self.report_id = json_data.get(ReportEnum.REPORT_ID)
        self.task_id = json_data.get(ReportEnum.TASK_ID)
        self.similar_report_num = json_data.get(AlgorithmEnum.SimilarityAlgoEnum.SIMILAR_REPORT_NUM, 5)  # 默认为5
        self.algorithm = json_data.get(AlgorithmEnum.ALGORITHM, AlgorithmEnum.SimilarityAlgoEnum.ReportSimilarityAlgorithm. \
                                       DEEP_SIMILARITY)  # 默认为DeepPrior
