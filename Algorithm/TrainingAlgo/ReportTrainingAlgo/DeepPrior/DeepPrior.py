import Algorithm.TrainingAlgo.ReportTrainingAlgo.DeepPrior.report_sim_matrix as rdm
import Algorithm.TrainingAlgo.ReportTrainingAlgo.DeepPrior.report_feature_extra as rfe
from Algorithm.TrainingAlgo.ReportTrainingAlgo.ReportTrainingStrategy import ReportTrainingStrategy


class DeepPrior(ReportTrainingStrategy):
    def __init__(self):
        pass

    def train_reports(self, report_file_path, task_id, report_sim_matrix_file_path, report_vec_file_path):
        # report feature extraction
        text_feature_list, widget_category_list, problem_widget_path_list = \
            rfe.extract_report_feature(report_file_path, task_id)
        # report sim matrix calculation
        rdm.cal_sim_matrix(report_file_path,  text_feature_list, widget_category_list,
                           problem_widget_path_list, report_sim_matrix_file_path, report_vec_file_path)
        return


if __name__ == '__main__':
    deepPrior = DeepPrior()
    deepPrior.train_reports()
