import abc


class ReportRecommendationStrategy(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get_recommended_reports(self, report_vec_file_path):
        pass
