from Utils.SymbolHandler import AlgorithmEnum, ReportEnum


class GetSimilarReportsVO(object):
    def __init__(self, report_id_similarity_tuple_list):
        res = []
        for k, v in report_id_similarity_tuple_list:
            item = {}
            item[ReportEnum.REPORT_ID] = k
            item[AlgorithmEnum.SimilarityAlgoEnum.SIMILARITY] = v
            res.append(item)

        self.val = res

    def get_value(self):
        '''
        这个类必须要有这个方法，因为定的接口返回值是arr不是obj...
        :return:
        '''
        return self.val
