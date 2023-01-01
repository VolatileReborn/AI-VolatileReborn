from Utils.SymbolHandler import ReportEnum


class ReportDAO(object):
    def __init__(self, reportId, task_id, img_url, defect_explanation, defect_reproduction_step, is_augmented, report_evaluation_value, is_evaluated):
        self.report_id = reportId
        self.task_id = task_id
        self.img_url = img_url
        self.defect_explanation = defect_explanation
        self.defect_reproduction_step = defect_reproduction_step

        self.is_augmented = is_augmented
        self.report_evaluation_value = report_evaluation_value
        self.is_evaluated = is_evaluated

    '''
    @param: report: 后端传过来的对象，(已经从json转成字典)
    '''
    @classmethod
    def createReportDAO(cls, report):
        reportId = report.get( ReportEnum.REPORT_ID )
        taskId = report.get(ReportEnum.TASK_ID)


        # 只使用第一张图片
        imgUrl = ( report.get( ReportEnum.DEFECT_PICTURE_LIST )[0] ).get(ReportEnum.DefectPictureEnum.IMG_URL)
        defectExplanation = report.get(ReportEnum.DEFECT_EXPLANATION)
        defectReproductionStep = report.get(ReportEnum.DEFECT_REPRODUCTION_STEP)

        is_augmented = report.get(ReportEnum.IS_AUGMENTED)
        report_evaluation_value = report.get(ReportEnum.REPORT_EVALUATION_VALUE)
        is_evaluated = report.get(ReportEnum.IS_EVALUATED)

        return ReportDAO( reportId, taskId, imgUrl, defectExplanation, defectReproductionStep, is_augmented, report_evaluation_value, is_evaluated )

