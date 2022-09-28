class ReportEnum():
    # 类属性
    REPORT = 'report'
    REPORT_ID = 'report_id'
    TASK_ID = 'task_id'
    RELATED_REPORTS = 'related_reports'
    DEFECT_EXPLANATION = 'defect_explanation'
    DEFECT_REPRODUCTION_STEP = 'defect_reproduction_step'
    DEFECT_PICTURE_LIST = 'defect_picture_list'

    class DefectPictureEnum:
        # 属于defect_picture_list
        IMG_URL = 'img_url'


class ReportVecEnum():
    REPORT_ID = 'report_id'
    X = 'x'
    Y = 'y'


class UserEnum():
    USER = 'user'
    USER_ID = 'user_id'


class TaskEnum():
    TASK_ID = "task_id"


class AlgorithmEnum:
    ALGORITHM = 'algorithm'

    class TrainingAlgoEnum:
        DEEP_PRIOR = 'DeepPrior'

    class SimilarityAlgoEnum:
        SIMILAR_REPORT_NUM = 'similar_report_num'
        SIMILARITY = 'similarity'

        class ReportSimilarityAlgorithm():
            DEEP_SIMILARITY = 'DeepSimilarity'
            TF_IDF = 'tf-idf'

    class RecommendationAlgoEnum:
        RECOMMENDATION_RULES = 'recommendation_rules'
        RECOMMENDED_TASK_NUM = 'recommended_task_num'
        RECOMMENDATION_THRESHOLD = 'recommendation_threshold'

        RECOMMENDED_REPORT_NUM = 'recommended_report_num'

        class ReportRecommendationAlgoEnum:
            DEEP_RECOMMENDATION = 'DeepRecommendation'

        class TaskRecommendationAlgoEnum:
            ITEM_CF = 'ItemCF'


