from Algorithm.RecommendationAlgo.ReportRecommendationAlgo.ReportRecommendationStrategy import \
    ReportRecommendationStrategy
from Algorithm.RecommendationAlgo.ReportRecommendationAlgo.DeepRecommendation.prioritization import prioritize


class DeepRecommendation(ReportRecommendationStrategy):

    def get_recommended_reports(self, report_sim_matrix_file_path):
        # report prioritization


        similar_report_id_list = prioritize(report_sim_matrix_file_path)

        # 将元素（report_id）转成int
        similar_report_id_list = list(map(int, similar_report_id_list))

        return similar_report_id_list
