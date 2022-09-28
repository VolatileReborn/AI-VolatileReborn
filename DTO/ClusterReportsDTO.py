from Utils.SymbolHandler import ReportEnum


class ClusterReportsDTO(object):
    def __init__(self, json_data):

        # 聚类是面向任务的， 同一任务下所有报告拥有相同的聚类，因此这个属性没用
        self.report_id = json_data.get(ReportEnum.REPORT_ID)

        self.task_id = json_data.get(ReportEnum.TASK_ID)
