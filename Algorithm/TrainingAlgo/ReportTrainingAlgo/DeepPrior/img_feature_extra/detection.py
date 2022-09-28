import cv2
import numpy as np

import Algorithm.TrainingAlgo.ReportTrainingAlgo.DeepPrior.img_feature_extra.draw as draw
from Algorithm.TrainingAlgo.ReportTrainingAlgo.DeepPrior.img_feature_extra.Component import Component
from Algorithm.TrainingAlgo.ReportTrainingAlgo.DeepPrior.img_feature_extra.Config import Config

C = Config()


def merge_text(compos, org_shape, max_word_gad=C.THRESHOLD_TEXT_MAX_WORD_GAP,
               max_word_height_ratio=C.THRESHOLD_TEXT_MAX_HEIGHT):
    def is_text_line(compo_a, compo_b):
        (col_min_a, row_min_a, col_max_a, row_max_a) = compo_a.put_bbox()
        (col_min_b, row_min_b, col_max_b, row_max_b) = compo_b.put_bbox()
        # on the same line
        if abs(row_min_a - row_min_b) < max_word_gad and abs(row_max_a - row_max_b) < max_word_gad:
            # close distance
            if abs(col_min_b - col_max_a) < max_word_gad or abs(col_min_a - col_max_b) < max_word_gad:
                return True
        return False

    changed = False
    new_compos = []
    row, col = org_shape[:2]
    for i in range(len(compos)):
        merged = False
        height = compos[i].height
        if height > 26:
            new_compos.append(compos[i])
            continue
        for j in range(len(new_compos)):
            if is_text_line(compos[i], new_compos[j]):
                new_compos[j].compo_merge(compos[i])
                merged = True
                changed = True
                break
        if not merged:
            new_compos.append(compos[i])

    if not changed:
        return compos
    else:
        return merge_text(new_compos, org_shape)


def rm_top_or_bottom_corners(components, org_shape, top_bottom_height=C.THRESHOLD_TOP_BOTTOM_BAR):
    new_compos = []
    height, width = org_shape[:2]
    for compo in components:
        (column_min, row_min, column_max, row_max) = compo.put_bbox()
        if not (row_max < height * top_bottom_height[0] or row_min > height * top_bottom_height[1]):
            new_compos.append(compo)
    return new_compos


def rm_line(binary,
            max_line_thickness=C.THRESHOLD_LINE_THICKNESS,
            min_line_length_ratio=C.THRESHOLD_LINE_MIN_LENGTH,
            show=False):
    width = binary.shape[1]
    thickness = 0
    gap = 0
    broad = np.zeros(binary.shape[:2], dtype=np.uint8)

    line_length = 0
    start, end = -1, -1
    for i, row in enumerate(binary):
        if (sum(row) / 255) / width > min_line_length_ratio:
            gap = 0
            if start == -1:
                start = i
            line_length = max(line_length, sum(row) / 255)
        else:
            if (sum(row) / 255) / width < 0.3:
                gap += 1
                if start != -1 and end == -1:
                    end = i
                if 0 < end - start < max_line_thickness and gap >= 1:
                    binary[start: end] = 0
                    start, end = -1, -1
            else:
                if 0 < end - start < max_line_thickness and gap >= 1:
                    binary[start: end] = 0
                start, end = -1, -1
    if show:
        cv2.imshow('no-line', binary)
        cv2.waitKey()


def compo_filter(compos, org):
    compos_new = []
    for compo in compos:
        # if compo.height < 26 and compo.width < 26:
        #    continue
        if compo.category == 'TextView' and compo.height > 100 and compo.width / org.shape[1] < 0.9:
            compo.category = 'ImageView'
        compos_new.append(compo)
    return compos_new


def component_detection(binary,
                        min_obj_area=C.THRESHOLD_OBJ_MIN_AREA,
                        line_thickness=C.THRESHOLD_LINE_THICKNESS,
                        min_rec_evenness=C.THRESHOLD_REC_MIN_EVENNESS,
                        max_dent_ratio=C.THRESHOLD_REC_MAX_DENT_RATIO,
                        step_h=5, step_v=2,
                        rec_detect=False, show=False, test=False):
    mask = np.zeros((binary.shape[0] + 2, binary.shape[1] + 2), dtype=np.uint8)
    compos_all = []
    compos_rec = []
    compos_nonrec = []
    row, column = binary.shape[0], binary.shape[1]
    for i in range(0, row, step_h):
        for j in range(i % 2, column, step_v):
            if binary[i, j] == 255 and mask[i, j] == 0:
                # get connected area
                mask_copy = mask.copy()
                cv2.floodFill(binary, mask, (j, i), None, 0, 0, cv2.FLOODFILL_MASK_ONLY)
                mask_copy = mask - mask_copy
                region = np.nonzero(mask_copy[1:-1, 1:-1])
                region = list(zip(region[0], region[1]))

                # ignore small area
                if len(region) < min_obj_area:
                    continue
                component = Component(region, binary.shape)
                # calculate the boundary of the connected area
                # ignore small area
                if component.width <= 3 or component.height <= 3:
                    continue
                if test:
                    print('Area:%d' % (len(region)))
                    draw.draw_boundary([component], binary.shape, show=True)

                if component.area > min_obj_area * 5 and component.compo_is_line(line_thickness):
                    continue
                compos_all.append(component)

                if rec_detect:
                    # rectangle check
                    if component.compo_is_rectangle(min_rec_evenness, max_dent_ratio):
                        component.rect_ = True
                        compos_rec.append(component)
                    else:
                        component.rect_ = False
                        compos_nonrec.append(component)

                if show:
                    print('Area:%d' % (len(region)))
                    draw.draw_boundary(compos_all, binary.shape, show=show)

    if rec_detect:
        return compos_rec, compos_nonrec
    else:
        return compos_all
