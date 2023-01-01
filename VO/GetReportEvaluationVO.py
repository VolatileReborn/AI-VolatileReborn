from Utils.SymbolHandler import ReportEnum


class GetReportEvaluationVO(object):
    def __init__(self, report_evaluation_value, is_evaluated):
        res = {
            ReportEnum.REPORT_EVALUATION_VALUE: report_evaluation_value,
            ReportEnum.IS_EVALUATED: is_evaluated
        }

        self.val = res

    def get_value(self):
        return self.val
