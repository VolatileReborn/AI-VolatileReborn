import cv2
from Algorithm.TrainingAlgo.ReportTrainingAlgo.DeepPrior.img_feature_extra.Component import Component


class Block(Component):
    def __init__(self, region, image_shape):
        super().__init__(region, image_shape)
        self.category = 'block'
        self.parent = None
        self.children = []
        self.uicompo_ = None
        self.top_or_botm = None

    def block_is_uicompo(self, image_shape, max_compo_scale):
        row, column = image_shape[:2]
        # ignore atomic components
        if self.bbox.height / row > max_compo_scale[0] or self.bbox.width / column > max_compo_scale[1]:
            return False
        return True

    def block_is_top_or_bottom_bar(self, image_shape, top_bottom_height):
        height, width = image_shape[:2]
        (column_min, row_min, column_max, row_max) = self.bbox.put_bbox()
        if column_min < 5 and row_min < 5 and \
                width - column_max < 5 and row_max < height * top_bottom_height[0]:
            self.uicompo_ = True
            return True
        if column_min < 5 and row_min > height * top_bottom_height[1] and \
                width - column_max < 5 and height - row_max < 5:
            self.uicompo_ = True
            return True
        return False

    def block_erase_from_bin(self, binary, pad):
        (column_min, row_min, column_max, row_max) = self.put_bbox()
        column_min = max(column_min - pad, 0)
        column_max = min(column_max + pad, binary.shape[1])
        row_min = max(row_min - pad, 0)
        row_max = min(row_max + pad, binary.shape[0])
        cv2.rectangle(binary, (column_min, row_min), (column_max, row_max), (0), -1)
