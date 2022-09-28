import abc


class ReportTrainingStrategy(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def train_reports(self, report_file_path, report_sim_matrix_file_path, report_vec_file_path ):
        pass