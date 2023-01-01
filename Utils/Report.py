class Report(object):
    '''
    Report Object
    '''
    def __init__(self, reportId, task_id, report_name,  defect_picture_list, img_url, defect_explanation, defect_reproduction_step, test_equipment_information, is_augmented, report_evaluation_value, is_evaluated):
        self.report_id = reportId
        self.task_id = task_id

        self.report_name = report_name

        self.defect_picture_list = defect_picture_list

        self.defect_explanation = defect_explanation
        self.defect_reproduction_step = defect_reproduction_step
        self.test_equipment_information = test_equipment_information

        self.is_augmented = is_augmented
        self.report_evaluation_value = report_evaluation_value
        self.is_evaluated = is_evaluated

    # class Defect_picture_list():
    #     def __init__(self,defect_picture_list):
    #         self.img_name = img_name
    #         self.img_url = img_url
    #         self.img_id = img_id

