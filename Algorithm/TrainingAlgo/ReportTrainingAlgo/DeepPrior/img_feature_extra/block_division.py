import cv2
import numpy as np
import Algorithm.TrainingAlgo.ReportTrainingAlgo.DeepPrior.img_feature_extra.draw as draw
from Algorithm.TrainingAlgo.ReportTrainingAlgo.DeepPrior.img_feature_extra.block import Block
from Algorithm.TrainingAlgo.ReportTrainingAlgo.DeepPrior.img_feature_extra.Config import Config
C = Config()


def block_hierarchy(blocks):
    for i in range(len(blocks) - 1):
        for j in range(i + 1, len(blocks)):
            relation = blocks[i].compo_relation(blocks[j])
            if relation == -1:
                blocks[j].children.append(i)
            if relation == 1:
                blocks[i].children.append(j)
    return


def block_bin_erase_all_blk(binary, blocks, pad=0, show=False):
    #erase the block parts from the binary map
    bin_org = binary.copy()
    for block in blocks:
        block.block_erase_from_bin(binary, pad)
    if show:
        cv2.imshow('before', bin_org)
        cv2.imshow('after', binary)
        cv2.waitKey()


def block_division(grey, org,
                   show=False, write_path=None,
                   step_h=10, step_v=10,
                   grad_thresh=C.THRESHOLD_BLOCK_GRADIENT,
                   line_thickness=C.THRESHOLD_LINE_THICKNESS,
                   min_rec_evenness=C.THRESHOLD_REC_MIN_EVENNESS,
                   max_dent_ratio=C.THRESHOLD_REC_MAX_DENT_RATIO,
                   min_block_height_ratio=C.THRESHOLD_BLOCK_MIN_HEIGHT):
    #divide image into block
    blocks = []
    mask = np.zeros((grey.shape[0]+2, grey.shape[1]+2), dtype=np.uint8)
    broad = np.zeros((grey.shape[0], grey.shape[1], 3), dtype=np.uint8)
    broad_all = broad.copy()

    row, column = grey.shape[0], grey.shape[1]
    for x in range(0, row, step_h):
        for y in range(0, column, step_v):
            if mask[x, y] == 0:
                mask_copy = mask.copy()
                cv2.floodFill(grey, mask, (y,x), None, grad_thresh, grad_thresh, cv2.FLOODFILL_MASK_ONLY)
                mask_copy = mask - mask_copy
                region = np.nonzero(mask_copy[1:-1, 1:-1])
                region = list(zip(region[0], region[1]))

                # ignore small regions
                if len(region) < 500:
                    continue
                block = Block(region, grey.shape)

                draw.draw_region(region, broad_all)
                if block.height < 40 and block.width < 40:
                    continue

                if block.compo_is_line(line_thickness):
                    continue

                if not block.compo_is_rectangle(min_rec_evenness, max_dent_ratio):
                    continue

                blocks.append(block)
                draw.draw_region(region, broad)
    if show:
        cv2.imshow('block', broad)
        cv2.waitKey(0)
    if write_path is not None:
        cv2.imwrite(write_path, broad)
    return blocks
