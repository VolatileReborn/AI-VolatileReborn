from Utils.SymbolHandler import ReportEnum


class GetReportEvaluationDTO():
    def __init__(self, json_data):
        # 要得到报告评估值的报告的id
        self.report = json_data.get(ReportEnum.REPORT)
        self.algorithm = json_data.get('algorithm')



