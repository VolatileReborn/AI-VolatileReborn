

class GetAugmentedReportsDTO(object):
    def __init__(self, json_data):
        self.augmented_report_num = json_data.get('augmented_report_num', 1)#需要扩增出的报告数量, 默认为1
        self.report = json_data.get('report')
        self.algorithm = json_data.get('algorithm', 'nlpaug') #默认为nlpaug
