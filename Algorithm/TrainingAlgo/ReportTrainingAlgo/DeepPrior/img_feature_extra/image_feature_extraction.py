import Algorithm.TrainingAlgo.ReportTrainingAlgo.DeepPrior.img_feature_extra.pre as pre
import Algorithm.TrainingAlgo.ReportTrainingAlgo.DeepPrior.img_feature_extra.block_division as blk
import Algorithm.TrainingAlgo.ReportTrainingAlgo.DeepPrior.img_feature_extra.detection as det
import Algorithm.TrainingAlgo.ReportTrainingAlgo.DeepPrior.img_feature_extra.Component as Compo
import Algorithm.TrainingAlgo.ReportTrainingAlgo.DeepPrior.img_feature_extra.draw as draw
from Algorithm.TrainingAlgo.ReportTrainingAlgo.DeepPrior.img_feature_extra.Config import Config
import cv2
import time
# from SimilarityAlgo.DeepPrior.img_feature_extra.CNN import CNN
import os
import numpy as np


def processing_block(org, binary, blocks, block_pad, C):
    image_shape = org.shape
    uicompos_all = []
    for block in blocks:
        if block.block_is_uicompo(image_shape, C.THRESHOLD_COMPO_MAX_SCALE):
            uicompos_all.append(block)
        binary_copy = binary.copy()
        for i in block.children:
            blocks[i].block_erase_from_bin(binary_copy, block_pad)
        block_clip_bin = block.compo_clipping(binary_copy, show=False)
        uicompos = det.component_detection(block_clip_bin, show=False)
        Compo.cvt_compos_relative_pos(uicompos, block.bbox.col_min, block.bbox.row_min)
        uicompos_all += uicompos
    return uicompos_all

def image_feature_extraction(img_path_list):
    C = Config()

    curpath = os.path.dirname(os.path.realpath(__file__))

    img_feature_list = []

    for img_file_path in img_path_list:
        print('---------begin analyze {}th img--------'.format(len(img_feature_list) + 1))
        start = time.perf_counter()
        num = 0

        # preprocessing
        org, grey = pre.read_img(img_file_path, 800)
        binary = pre.binarization(org, show=False, write_path=None)
        binary_org = binary.copy()

        # segment image and detect components
        blocks = blk.block_division(grey, org, show=False, write_path=None)
        blk.block_hierarchy(blocks)
        uicompos_in_blk = processing_block(org, binary, blocks, 4, C)

        det.rm_line(binary)
        blk.block_bin_erase_all_blk(binary, blocks, 4, show=False)
        uicompos_not_in_blk = det.component_detection(binary)
        uicompos = uicompos_in_blk + uicompos_not_in_blk  # uicompos就是一个widget,是多个原子widget的组合

        uicompos = det.merge_text(uicompos, org.shape)
        draw.draw_bounding_box_plt(org, uicompos, show=False)

        # save components image to local
        k = 0
        board = org.copy()

        path_split = img_file_path.split('\\')
        file_name = path_split[len(path_split) - 1]
        index = file_name.split('.')[0]
        if not os.path.exists(os.path.join(curpath, 'Compos', index)):
            os.mkdir(os.path.join(curpath, 'Compos', index))

        compo_paths = []

        for compo in uicompos:
            print('yes')
            bbox = compo.put_bbox()
            i = board[bbox[1]:bbox[3], bbox[0]:bbox[2]]
            cv2.imwrite(os.path.join(curpath, 'Compos', index, str(k) + '.png'), i,
                        [cv2.IMWRITE_PNG_COMPRESSION, 0])
            print(os.path.join(curpath, 'Compos', index, str(k) + '.png'))
            compo_paths.append(os.path.join(curpath, 'Compos', index, str(k) + '.png'))
            k += 1

        Compo.compos_containment(uicompos)

        # 随便搞的
        compo_category = {'Button': 0, 'CheckBox': 0, 'CheckedTextView': 0, 'EditText': 0, 'ImageButton': 0,
                          'ImageView': 0,
                          'ProgressBar': 0, 'ProgressBarHorizontal': 0, 'ProgressBarVertical': 0, 'RadioButton': 0,
                          'RatingBar': 0, 'SeekBar': 0, 'Switch': 0, 'Spinner': 0, 'TextView': 0}
        compo_category_vec = np.array(list(compo_category.values()))
        img_feature_list.append({'compo_paths': compo_paths, 'compo_categories': compo_category_vec})

        print('-----------finish analyzing number{} img--------------'.format(len(img_feature_list)))
    return img_feature_list




#
#
# # image_feature：{ 'compo_paths': compo_paths, 'compo_categories': {14维向量} }
# def image_feature_extraction(img_path_list):
#     C = Config()
#     cnn = CNN()
#
#     curpath = os.path.dirname(os.path.realpath(__file__))
#
#     img_feature_list = []
#
#     for img_file_path in img_path_list:
#         print('---------begin analyze {}th img--------'.format(len(img_feature_list) + 1))
#         start = time.clock()
#         num = 0
#
#         # preprocessing
#         org, grey = pre.read_img(img_file_path, 800)
#         binary = pre.binarization(org, show=False, write_path=None)
#         binary_org = binary.copy()
#
#         # segment image and detect components
#         blocks = blk.block_division(grey, org, show=False, write_path=None)
#         blk.block_hierarchy(blocks)
#         uicompos_in_blk = processing_block(org, binary, blocks, 4, C)
#
#         det.rm_line(binary)
#         blk.block_bin_erase_all_blk(binary, blocks, 4, show=False)
#         uicompos_not_in_blk = det.component_detection(binary)
#         uicompos = uicompos_in_blk + uicompos_not_in_blk # uicompos就是一个widget,是多个原子widget的组合
#
#         uicompos = det.merge_text(uicompos, org.shape)
#         draw.draw_bounding_box_plt(org, uicompos, show=False)
#
#         # save components image to local
#         k = 0
#         board = org.copy()
#
#         path_split = img_file_path.split('\\')
#         file_name = path_split[len(path_split) - 1]
#         index = file_name.split('.')[0]
#         if not os.path.exists(os.path.join(curpath, 'Compos', index)):
#             os.mkdir(os.path.join(curpath, 'Compos', index))
#
#         compo_paths = []
#
#         for compo in uicompos:
#             print('yes')
#             bbox = compo.put_bbox()
#             i = board[bbox[1]:bbox[3], bbox[0]:bbox[2]]
#             cv2.imwrite(os.path.join(curpath, 'Compos', index, str(k) + '.png'), i,
#                         [cv2.IMWRITE_PNG_COMPRESSION, 0])
#             print(os.path.join(curpath, 'Compos', index, str(k) + '.png'))
#             compo_paths.append(os.path.join(curpath, 'Compos', index, str(k) + '.png'))
#             k += 1
#
#         Compo.compos_containment(uicompos)
#
#         # components classification
#         cnn.predict(seg.clipping(org, uicompos), uicompos, show=False)
#         uicompos = det.compo_filter(uicompos, org)
#         image = draw.draw_bounding_box_class_plt(org, uicompos, os.path.join(curpath, 'Compos', index), show=True)
#         print("[Compo Detection Completed in %.3f s] %d %s" % (time.clock() - start, num, img_file_path))
#
#         compo_category = {'Button': 0, 'CheckBox': 0, 'CheckedTextView': 0, 'EditText': 0, 'ImageButton': 0,
#                           'ImageView': 0,
#                           'ProgressBar': 0, 'ProgressBarHorizontal': 0, 'ProgressBarVertical': 0, 'RadioButton': 0,
#                           'RatingBar': 0, 'SeekBar': 0, 'Switch': 0, 'Spinner': 0, 'TextView': 0}
#         for compo in uicompos:
#             compo_category[str(compo.category)] = compo_category[str(compo.category)] + 1
#
#         compo_category_vec = np.array(list(compo_category.values()))
#         img_feature_list.append({'compo_paths': compo_paths, 'compo_categories': compo_category_vec})
#         print('-----------finish analyzing number{} img--------------'.format(len(img_feature_list)))
#
#         show = False
#         if show:
#             cv2.destroyAllWindows()
#
#     return img_feature_list
