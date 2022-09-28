from Utils.SymbolHandler import ReportEnum, AlgorithmEnum


class GetRecommendedReportsDTO(object):
    def __init__(self, json_data):
        # 要被比较的报告的id, 由于推荐算法没有用到该字段（DeepSimilarity对同一任务下的所有报告，返回相同的结果), 该字段暂时没用
        self.report_id = json_data.get(ReportEnum.REPORT_ID)
        self.task_id = json_data.get(ReportEnum.TASK_ID)
        self.recommended_report_num = json_data.get(AlgorithmEnum.RecommendationAlgoEnum.RECOMMENDED_REPORT_NUM,
                                                    5)  # 默认为5
        self.algorithm = json_data.get(AlgorithmEnum.ALGORITHM,
                                       AlgorithmEnum.RecommendationAlgoEnum.ReportRecommendationAlgoEnum. \
                                       DEEP_RECOMMENDATION)  # 默认为DeepRecommendation
