import abc


class TaskRecommendationStrategy(metaclass=abc.ABCMeta):
    RECOMMENDATION_DEGREE = "recommendation_degree"

    @abc.abstractmethod
    def get_top_n_recommended_tasks(self, userIdToBeRecommended, recommendationRules, recommendedTaskNum, recommendationThreshold):
        pass