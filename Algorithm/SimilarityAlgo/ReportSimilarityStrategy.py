import abc


class ReportSimilarityStrategy(metaclass=abc.ABCMeta):
    def __init__(self):
        return

    @abc.abstractmethod
    def get_similar_reports(self, report_id, report_sim_matrix_file_path):
        pass
