class ReportEnum():
    # 类属性
    REPORT = 'report'
    REPORT_ID = 'report_id'
    REPORT_NAME = 'report_name'

    TASK_ID = 'task_id'
    RELATED_REPORTS = 'related_reports'
    DEFECT_EXPLANATION = 'defect_explanation'
    DEFECT_REPRODUCTION_STEP = 'defect_reproduction_step'
    TEST_EQUIPMENT_INFORMATION = 'test_equipment_information'
    DEFECT_PICTURE_LIST = 'defect_picture_list'

    IS_AUGMENTED = 'is_augmented'
    REPORT_EVALUATION_VALUE = 'report_evaluation_value' # 报告的自动化质量评估值
    IS_EVALUATED = 'is_evaluated' # 报告是否被评估. 仅当该字段为true时, 报告的质量评估值才有效

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

    class AugmentationEnum:
        NLPAUG = 'nlpaug'

    class EvaluationEnum:
        SIMPLE_EVA = 'SimpleEva'


