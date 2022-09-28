from Utils.SymbolHandler import ReportEnum, AlgorithmEnum

class PrepareReportTrainingDataDTO():
    def __init__(self, json_data):
        self.report_list = json_data.get('report_list')
        self.task_id = json_data.get(ReportEnum.TASK_ID)
        self.algorithm = json_data.get(AlgorithmEnum.ALGORITHM, AlgorithmEnum.TrainingAlgoEnum.DEEP_PRIOR)