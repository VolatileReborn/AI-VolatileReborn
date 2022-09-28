from Utils.SymbolHandler import ReportEnum


class ReportVecDAO(object):
    def __init__(self, report_id, report_vec):
        self.report_id = report_id

        self.X = report_vec[0]
        self.Y = report_vec[1]
