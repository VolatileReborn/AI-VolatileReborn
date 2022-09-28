
from Utils.SymbolHandler import UserEnum, AlgorithmEnum



class GetRecommendedTasksDTO(object):
    def __init__(self, json_data):
        self.user = json_data.get(UserEnum.USER, {})
        self.recommendation_rules = json_data.get(AlgorithmEnum.RecommendationAlgoEnum.RECOMMENDATION_RULES, {})
        self.recommended_task_num = json_data.get(AlgorithmEnum.RecommendationAlgoEnum.RECOMMENDED_TASK_NUM, 5)  # 默认为5
        self.algorithm = json_data.get(AlgorithmEnum.ALGORITHM, AlgorithmEnum.RecommendationAlgoEnum.\
                                  TaskRecommendationAlgoEnum.ITEM_CF) # 默认为"ItemCF"
        self.recommendation_threshold = json_data.get(AlgorithmEnum.RecommendationAlgoEnum.RECOMMENDATION_THRESHOLD, 0.1)  # 默认为0.1