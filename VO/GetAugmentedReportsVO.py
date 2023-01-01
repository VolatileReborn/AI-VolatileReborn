from Utils.SymbolHandler import ReportEnum


class GetAugmentedReportsVO(object):
    def __init__(self, report_list_len, defect_explanation_list, defect_reproduction_step_list, test_equipment_information_list, report_name_list):
        augmented_report_list = list()

        for i in range(0, report_list_len):
            augmented_report = {
                ReportEnum.DEFECT_EXPLANATION: defect_explanation_list[i],
                ReportEnum.DEFECT_REPRODUCTION_STEP: defect_reproduction_step_list[i],
                ReportEnum.TEST_EQUIPMENT_INFORMATION: test_equipment_information_list[i],
                ReportEnum.REPORT_NAME: report_name_list[i]
            }
            augmented_report_list.append(augmented_report)


        self.val = augmented_report_list

    def get_value(self):
        return self.val

