import random

import Algorithm.TrainingAlgo.ReportTrainingAlgo.DeepPrior.text_feature_extra.dtw as dtw
import numpy as np
import jieba
import os
import gensim
import cv2
import csv
import pandas as pd

# SR = gamma * SB + delta * SC (SR: sim between reports)
# SB = alpha1 * SP + beta1 * SWP (SB: Bug sim, SP: bug descriptions sim，SWP：problem widget images sim）
# SC = alpha2 * SR + beta2 * SWC (SC: Context sim, SR：reproduction steps sim，SWC: widget categories sim）

# default: gamma = delta = alpha1 = alpha2 = beta1 = beta2 = 0.5
from Mapper.ReportVecMapper import ReportVecMapper
from Utils.SymbolHandler import ReportEnum

gamma = 0.9
delta = 0.1 # CFT的权重，暂时调低

alpha1 = 0.8
beta1 = 0.2 # problem widget的权重，图片不靠谱，所以权重低一点

alpha2 = 1
beta2 = 0  # 因为context widget的分类没有实现，context widget的向量就没有意义，其相似度计算就没有意义，这里将其权重置为0

# initial widget categories vector of blank report
initial_widget_categories = np.zeros(15)
# initial reproduction steps list of blank report
initial_reproduction_procedures = ['']
# initial bug descriptions list of blank report
initial_bug_descriptions = ['']

curPath = os.path.dirname(os.path.realpath(__file__))

# pre-trained word2ve model
word2vec_model = gensim.models.Word2Vec.load(os.path.join(curPath, 'text_feature_extra/bugdata_format_model_100'))


# sim between two short sentences (measured by euclidean distance)
# bug description的相似度，即Sim_P
# 用了word2vec( model参数实际传入的算法是word2vec )
def sentence_sim(model, s1, s2):
    size = model.layer1_size

    def sentence_vector(s):
        words = []
        try:
            words = [x for x in jieba.cut(s, cut_all=True) if x != '']
        except:
            return np.zeros(size)
        v = np.zeros(size)
        length = len(words)
        for word in words:
            try:
                idx = model.wv.key_to_index[word]
                v[idx] += 1
            except:
                length -= 1
        if length == 0:
            return np.zeros(size)
        v /= length
        return v

    v1, v2 = sentence_vector(s1), sentence_vector(s2)
    dis = eucli_distance(v1, v2)
    return 1 - dis


def eucli_distance(a, b):
    dis = np.sqrt(sum(np.power((a - b), 2)))
    return round(dis, 4)


# To extract the image features, we adopt the state-of-the-art SIFT (Scale-Invariant Feature Transform) algorithm [10].
# Therefore, each widget is represented by a feature point set.
# 读取两个path代表的图片，计算使用FLANN其sift距离
def sift_similarity(path1, path2):
    # get matched feature points nums
    def get_match_num(matches, ratio):
        matches_mask = [[0, 0] for i in range(len(matches))]
        match_num = 0
        for i, (m, n) in enumerate(matches):
            if m.distance < ratio * n.distance:  # 将距离比率小于ratio的匹配点删选出来
                matches_mask[i] = [1, 0]
                match_num += 1
        return (match_num, matches_mask)

    # create SIFT feature extractor
    sift = cv2.SIFT_create()
    # sift = cv2.xfeatures2d.SIFT_create()

    # create FLANN match object
    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)

    # To compare and match the problem widgets from different crowdsourced test reports, we use the FLANN Library
    flann = cv2.FlannBasedMatcher(index_params, search_params)

    if path1 == '':
        # if both path1 and path2 equal ''
        # return 0
        if path2 == '':
            return 0
        # if path1 equals '' but path2 not equals ''
        # return the feature points num of path2
        else:
            format_path2 = '/'.join(path2.split("\\"))
            image2 = cv2.imread(format_path2, 0)
            print('format_path2:{}'.format(format_path2))
            height2, width2 = image2.shape[:2]
            imagenew2 = cv2.resize(image2, (2 * width2, 2 * height2), interpolation=cv2.INTER_CUBIC)
            kp2, des2 = sift.detectAndCompute(imagenew2, None)
            if kp2 is not None:
                return round(len(kp2), 4)
            else:
                return 0
    else:
        # if path2 equals '' but path1 not equals ''
        # return the feature points num of path1
        format_path1 = '/'.join(path1.split("\\"))
        image1 = cv2.imread(format_path1, 0)
        print('format_path1:{}'.format(format_path1))
        height1, width1 = image1.shape[:2]
        imagenew1 = cv2.resize(image1, (2 * width1, 2 * height1), interpolation=cv2.INTER_CUBIC)
        kp1, des1 = sift.detectAndCompute(imagenew1, None)
        if path2 == '':
            if kp1 is not None:
                return round(len(kp1), 4)
            else:
                return 0
        else:
            # if neither path1 or path2 equals ''
            # return the match feature points of two images
            format_path2 = '/'.join(path2.split("\\"))
            image2 = cv2.imread(format_path2, 0)
            print('format_path2:{}'.format(format_path2))
            height2, width2 = image2.shape[:2]
            imagenew2 = cv2.resize(image2, (2 * width2, 2 * height2), interpolation=cv2.INTER_CUBIC)
            kp2, des2 = sift.detectAndCompute(imagenew2, None)
            try:
                # match feature points
                # set k = 2, for each image two matches will return
                matches = flann.knnMatch(des1, des2, k=2)
                # cal match by ratio
                (matchNum, matchesMask) = get_match_num(matches, 0.9)
                if len(matches) == 0:
                    print('ratio is 0')
                    return 0
                else:
                    match_ratio = matchNum / len(matches)
                    print('ratio：', match_ratio)
                    return round(match_ratio, 4)
            except Exception as ex:
                pass
                return 0


# get feature points num of images
# To extract the image features, we adopt the state-of-the-art SIFT (Scale-Invariant Feature Transform) algorithm [10].
# Therefore, each widget is represented by a feature point set.
# 见 https://www.jianshu.com/p/65a56a2f63e3
def get_fea_num(path):
    if path == '':
        return 0
    sift = cv2.SIFT_create()
    format_path = '/'.join(path.split("\\"))
    image = cv2.imread(format_path, 0)
    height, width = image.shape[:2]
    imagenew = cv2.resize(image, (2 * width, 2 * height), interpolation=cv2.INTER_CUBIC)
    kp1, des1 = sift.detectAndCompute(imagenew, None)
    return len(kp1)


def normalize_dis(dis, max_dis, min_dis):
    '''
    # normalize distance to [0,1] by max_dis and min_dis
    事实证明没用
    :param dis:
    :param max_dis:
    :param min_dis:
    :return:
    '''
    if (max_dis - min_dis) == 0:
        return 0
    else:
        return dis
        # return (dis - min_dis) / (max_dis - min_dis)


# SR = gamma * SB + delta * SC
def cal_report_similarity(text_feature1, widget_category1, pwidget_img1, text_feature2, widget_category2,
                          pwidget_img2, index1, index2, max_sift_fea, max_problem_dis, min_problem_dis,
                          max_procedure_dis, min_procedure_dis, max_category_dis, min_category_dis):
    SB, SC = cal_report_similarity_vec(text_feature1, widget_category1, pwidget_img1, text_feature2, widget_category2,
                          pwidget_img2, index1, index2, max_sift_fea, max_problem_dis, min_problem_dis,
                          max_procedure_dis, min_procedure_dis, max_category_dis, min_category_dis)
    SR = gamma * SB + delta * SC
    print('---------finish cal {}th & {}th report sim, Sim_report = {}---------'.format(index1, index2, SR))
    return round(SR, 4)

    # print('---------begin cal {}th & {}th report sim---------'.format(index1, index2))
    # print('---{}th text_feature{}---'.format(index1, text_feature1))
    # print('---{}th text_feature{}---'.format(index2, text_feature2))
    # SB = cal_bug_similarity(pwidget_img1, text_feature1, pwidget_img2, text_feature2, max_sift_fea, max_problem_dis,
    #                         min_problem_dis)
    # if SB == -1 or SB == -2:
    #     return SB
    # SC = cal_context_similarity(widget_category1, text_feature1, widget_category2, text_feature2, max_procedure_dis,
    #                             min_procedure_dis, max_category_dis, min_category_dis)
    # SR = gamma * SB + delta * SC
    # print('---------finish cal {}th & {}th report sim---------'.format(index1, index2))
    #
    # return round(SR, 4)


def cal_report_similarity_vec(text_feature1, widget_category1, pwidget_img1, text_feature2, widget_category2,
                              pwidget_img2, index1, index2, max_sift_fea, max_problem_dis, min_problem_dis,
                              max_procedure_dis, min_procedure_dis, max_category_dis, min_category_dis):
    '''
    计算报告的相似特征向量
    :param text_feature1:
    :param widget_category1:
    :param pwidget_img1:
    :param text_feature2:
    :param widget_category2:
    :param pwidget_img2:
    :param index1:
    :param index2:
    :param max_sift_fea:
    :param max_problem_dis:
    :param min_problem_dis:
    :param max_procedure_dis:
    :param min_procedure_dis:
    :param max_category_dis:
    :param min_category_dis:
    :return:
    '''
    print('---------begin cal {}th & {}th report sim---------'.format(index1, index2))
    print('---{}th text_feature{}---'.format(index1, text_feature1))
    print('---{}th text_feature{}---'.format(index2, text_feature2))
    SB = cal_bug_similarity(pwidget_img1, text_feature1, pwidget_img2, text_feature2, max_sift_fea, max_problem_dis,
                            min_problem_dis)
    if SB == -1 or SB == -2:
        return SB
    SC = cal_context_similarity(widget_category1, text_feature1, widget_category2, text_feature2, max_procedure_dis,
                                min_procedure_dis, max_category_dis, min_category_dis)
    # SR = gamma * SB + delta * SC
    print('---------finish cal {}th & {}th report sim vec, Sim_BFT = {}, Sim_CFT = {}---------'.format(index1, index2, SB, SC))

    return SB, SC


# SB = alpha1 * SP + beta1 * SWP
def cal_bug_similarity(pwidget_img1, text_feature1, pwidget_img2, text_feature2, max_sift_fea, max_problem_dis,
                       min_problem_dis):
    '''

    :param pwidget_img1:
    :param text_feature1:
    :param pwidget_img2:
    :param text_feature2:
    :param max_sift_fea:
    :param max_problem_dis:
    :param min_problem_dis:
    :param isSimple: True： 不算图片了
    :return:
    '''
    problem_list1 = text_feature1['problems_list']
    problem1 = ' '.join(problem_list1)
    problem2 = ''
    if text_feature2 is not None:
        problem_list2 = text_feature2['problems_list']
        problem2 = ' '.join(problem_list2)


    sift_sim = sift_similarity(pwidget_img1, pwidget_img2)
    SWP = sift_sim


    # SWP = normalize_dis(sift_sim, max_sift_fea, 0) # 这个归一化似乎有问题
    if SWP == -1 or SWP == -2:
        return SWP

    word2vec_sim = sentence_sim(word2vec_model, problem1, problem2)
    SP = normalize_dis(word2vec_sim, max_problem_dis, min_problem_dis)

    if pwidget_img1 == "" or pwidget_img2 == "":
        # 缺陷图片为空（说明没找到缺陷图片），则直接将bug description相似度作为BFT相似度
        SB = SP
    else:
        SB = alpha1 * SP + beta1 * SWP
    print('Sim_problem_widget:{}, Sim_problem:{}'.format(SWP, SP))
    return SB


# SC = alpha2 * SR + beta2 * SWC
# 即 Sim_{CFT} =\alpha ∗ Sim_{W_C} +(1−α) ∗ Sim_R
def cal_context_similarity(category_vec1, text_feature1, category_vec2, text_feature2, max_procedure_dis,
                           min_procedure_dis, max_category_dis, min_category_dis):
    '''
    dtw算法怎么算都是完全相似，因此这里的SR暂且用随机值，相应的相似度计算的时候把S_BFT的权重调低
    :param category_vec1:
    :param text_feature1:
    :param category_vec2:
    :param text_feature2:
    :param max_procedure_dis:
    :param min_procedure_dis:
    :param max_category_dis:
    :param min_category_dis:
    :return:
    '''
    procedures_list1 = text_feature1['procedures_list']
    procedures_list2 = initial_reproduction_procedures
    if text_feature2 is not None:
        procedures_list2 = text_feature2['procedures_list']

    # DTW距离不准，这里用文本相似度来计算SR
    # sim = 1 - dis
    # we adopt the Dynamic Time Warping (DTW) [12] algorithm to process the to-compare “action-object” sequence
    # SR = 1.0 - dtw.dtw_distance(procedures_list1, procedures_list2, min_procedure_dis,
    #                             max_procedure_dis, isOneValue=True)
    # 暂且用文本相似度
    procedures_1_text = "".join(procedures_list1)
    procedures_2_text = "".join(procedures_list2)
    SR = normalize_dis(sentence_sim(word2vec_model, procedures_1_text, procedures_2_text), max_procedure_dis, min_procedure_dis)

    # cal dis between two widget category vec
    dis = normalize_dis(eucli_distance(category_vec1, category_vec2), max_category_dis, min_category_dis)
    SWC = 1.0 - round(dis, 4)
    SC = alpha2 * SR + beta2 * SWC
    print(procedures_list1, procedures_list2)
    print('Sim_reproduction_step:{},Sim_context_widget:{}'.format(SR, SWC))
    return SC


# get max and min value of four types of different distance
def cal_normalize_dis(number, problem_widget_path_list, text_feature_list, widget_category_list):
    # the max num of sift feature points of screenshots (used to normalize dis)
    max_sift_fea = 0.
    # the max val of Euclidean distance of two bug descriptions (used to normalize dis)
    max_problem_dis = 0.
    # the min val of Euclidean distance of two bug descriptions (used to normalize dis)
    min_problem_dis = 100000.
    # the max val of Euclidean distance of two reproduction steps (used to normalize dis) 用于计算reproduction的相似度
    max_procedure_dis = 0.
    # the min val of Euclidean distance of two reproduction steps (used to normalize dis)
    min_procedure_dis = 100000.
    # the max val of Euclidean distance of two widget categories vectors (used to normalize dis)
    max_category_dis = 0.
    # the min val of Euclidean distance of two widget categories vectors (used to normalize dis)
    min_category_dis = 100000.
    for i in range(0, len(number)):
        # cal dis between each report and blank report
        print('-------------start cal sim between {}th & -1 report-----------'.format(number[i]))
        fea_num = get_fea_num(problem_widget_path_list[i])
        if fea_num > max_sift_fea:
            max_sift_fea = fea_num
        text_feature = text_feature_list[i]
        problem_list = text_feature['problems_list']
        print('-----------{}th report problem_list:{}'.format(number[i], problem_list))
        problem = ' '.join(problem_list)
        problem_sim = sentence_sim(word2vec_model, problem, '')
        if problem_sim > max_problem_dis:
            max_problem_dis = problem_sim
        if problem_sim < min_problem_dis:
            min_problem_dis = problem_sim
        procedures_list = text_feature['procedures_list']
        print('-----------{}th report procedure_list:{}'.format(number[i], procedures_list))
        min_dtw_dis, max_dtw_dis = dtw.dtw_distance(procedures_list, initial_reproduction_procedures, 0, 0)
        if min_dtw_dis < min_procedure_dis:
            min_procedure_dis = min_dtw_dis
        if max_dtw_dis > max_procedure_dis:
            max_procedure_dis = max_dtw_dis
        eucli_dis = eucli_distance(widget_category_list[i], initial_widget_categories)
        if eucli_dis > max_category_dis:
            max_category_dis = eucli_dis
        if eucli_dis < min_category_dis:
            min_category_dis = eucli_dis
        print('-------------end cal sim between {}th & -1 report-----------'.format(number[i]))
    # cal dis between every two reports in report list
    for i in range(0, len(number) - 1):
        for j in range(i + 1, len(number)):
            print('-------------start cal sim between {}th & {}th report-----------'.format(number[i], number[j]))
            text_feature1 = text_feature_list[i]
            problem_list1 = text_feature1['problems_list']
            problem1 = ' '.join(problem_list1)
            text_feature2 = text_feature_list[j]
            problem_list2 = text_feature2['problems_list']
            print('-----------{}th report problem_list:{}'.format(number[i], problem_list1))
            print('-----------{}th report problem_list:{}'.format(number[j], problem_list2))
            problem2 = ' '.join(problem_list2)
            problem_sim = sentence_sim(word2vec_model, problem1, problem2)
            if problem_sim > max_problem_dis:
                max_problem_dis = problem_sim
            if problem_sim < min_problem_dis:
                min_problem_dis = problem_sim
            procedures_list1 = text_feature1['procedures_list']
            procedures_list2 = text_feature2['procedures_list']
            print('-----------{}th report procedure_list:{}'.format(number[i], procedures_list1))
            print('-----------{}th report procedure_list:{}'.format(number[i], procedures_list2))
            min_dtw_dis, max_dtw_dis = dtw.dtw_distance(procedures_list1, procedures_list2, 0, 0)
            if min_dtw_dis < min_procedure_dis:
                min_procedure_dis = min_dtw_dis
            if max_dtw_dis > max_procedure_dis:
                max_procedure_dis = max_dtw_dis
            eucli_dis = eucli_distance(widget_category_list[i], widget_category_list[j])
            if eucli_dis > max_category_dis:
                max_category_dis = eucli_dis
            if eucli_dis < min_category_dis:
                min_category_dis = eucli_dis
            print('-------------start cal sim between {}th & {}th report-----------'.format(number[i], number[j]))
    print('max_sift={},max_problem={},min_problem={},max_procedure={},min_procedure={},max_category={},'
          'min_category={}'.format(max_sift_fea, max_problem_dis, min_problem_dis, max_procedure_dis, min_procedure_dis,
                                   max_category_dis, min_category_dis))
    return max_sift_fea, max_problem_dis, min_problem_dis, max_procedure_dis, min_procedure_dis, max_category_dis, min_category_dis


def cal_sim_matrix(report_file_path, text_feature_list, widget_category_list, problem_widget_path_list,
                   report_sim_matrix_file_path, report_vec_file_path):
    '''
    # calculate and record sim between every two reports in report list
    计算相似度矩阵和报告的相似度向量，分别存入对应文件

    :param report_file_path: report数据所在文件
    :param text_feature_list:
    :param widget_category_list:
    :param problem_widget_path_list:
    :param report_sim_matrix_file_path: 相似度矩阵存入该文件
    :param report_vec_file_path: 报告转化成的向量存入该文件
    :return:
    '''
    reports = pd.read_csv(report_file_path)
    report_ids = list(reports[ReportEnum.REPORT_ID])  # 报告id的列表

    # get max and min value of distance (used for distance normalization)
    max_sift_fea, max_problem_dis, min_problem_dis, max_procedure_dis, min_procedure_dis, max_category_dis, \
    min_category_dis = cal_normalize_dis(report_ids, problem_widget_path_list, text_feature_list, widget_category_list)

    file = open(report_sim_matrix_file_path, 'w', encoding='utf-8', newline='')
    csv_writer = csv.writer(file)
    header = ['index', '-1']
    for report_id in report_ids:
        header.append(str(report_id))
    csv_writer.writerow(header)  # 矩阵的header， 形如 index,-1, [report_id], [report_id], [report_id]
    sim_matrix = np.zeros((len(report_ids) + 1, len(report_ids) + 1))
    sim_matrix[0][0] = 1
    for i in range(0, len(report_ids)):
        # cal normalized sim between each report and blank report
        # 空报告的report_id为-1
        sim = cal_report_similarity(text_feature_list[i], widget_category_list[i],
                                    problem_widget_path_list[i], None, initial_widget_categories, '',
                                    report_ids[i], -1, max_sift_fea, max_problem_dis, min_problem_dis,
                                    max_procedure_dis,
                                    min_procedure_dis, max_category_dis, min_category_dis)

        # sim between report i and report j is equal to sim between report j and report i.
        sim_matrix[i + 1][0] = sim
        sim_matrix[0][i + 1] = sim
    # cal sim between every two report in report list
    # 由于第一行和第一列是和空报告做对比，该位置被占据。
    # 假设是第零和第一篇report做对比，其结果应该存在相似矩阵的[ 0+1, 1+1 ]
    for i in range(0, len(report_ids)):
        for j in range(i, len(report_ids)):
            last_report_id_idx = len(report_ids) - 1


            if i == j:
                sim_matrix[i + 1][j + 1] = 1

                # 最后一篇报告的相似度，肯定是1
                if i == last_report_id_idx:
                    save_totally_same_report_vec(report_ids[i], report_vec_file_path)


            else:
                sim = cal_report_similarity(text_feature_list[i], widget_category_list[i], problem_widget_path_list[i],
                                            text_feature_list[j], widget_category_list[j], problem_widget_path_list[j],
                                            report_ids[i], report_ids[j], max_sift_fea, max_problem_dis,
                                            min_problem_dis,
                                            max_procedure_dis, min_procedure_dis, max_category_dis, min_category_dis)
                # 将列表里最后一个报告作为基准报告， 所有报告相对于基准报告的相似度（二维向量表示），就作为该报告的绝对相似度
                # 这意味着最后一篇报告没有相似度
                if j == last_report_id_idx:

                    cal_sim_vec(text_feature_list[i], widget_category_list[i], problem_widget_path_list[i],
                                text_feature_list[j], widget_category_list[j], problem_widget_path_list[j],
                                report_ids[i], report_ids[j], max_sift_fea, max_problem_dis, min_problem_dis,
                                max_procedure_dis, min_procedure_dis, max_category_dis, min_category_dis,
                                report_vec_file_path)

                sim_matrix[i + 1][j + 1] = sim
                sim_matrix[j + 1][i + 1] = sim
    # record sim result in .csv file
    for i in range(0, len(report_ids) + 1):
        index = 0
        if i == 0:
            index = -1
        else:
            index = report_ids[i - 1]
        sim = [str(index)]
        for j in range(0, len(report_ids) + 1):
            sim.append(str(sim_matrix[i][j]))
        csv_writer.writerow(sim)
    file.close()


def cal_sim_vec(text_feature_1, widget_category_1, problem_widget_path_1,
                text_feature_2, widget_category_2, problem_widget_path_2,
                report_id_1, report_id_2, max_sift_fea, max_problem_dis, min_problem_dis,
                max_procedure_dis, min_procedure_dis, max_category_dis, min_category_dis, report_vec_file_path):
    '''
    计算并存储report_1相对于report_2的相似度特征向量

    :param text_feature_1:
    :param widget_category_1:
    :param problem_widget_path_1:
    :param text_feature_2:
    :param widget_category_2:
    :param problem_widget_path_2:
    :param report_id_1:
    :param report_id_2:
    :param max_sift_fea:
    :param max_problem_dis:
    :param min_problem_dis:
    :param max_procedure_dis:
    :param min_procedure_dis:
    :param max_category_dis:
    :param min_category_dis:
    :param report_vec_file_path:
    :return:
    '''
    report_vec = np.zeros(2)
    SB, SC = cal_report_similarity_vec(text_feature_1, widget_category_1, problem_widget_path_1,
                                       text_feature_2, widget_category_2, problem_widget_path_2,
                                       report_id_1, report_id_2, max_sift_fea, max_problem_dis, min_problem_dis,
                                       max_procedure_dis, min_procedure_dis, max_category_dis, min_category_dis)
    # 必须是正数
    report_vec[0] = abs(SB)
    report_vec[1] = abs(SC)

    report_id = report_id_1
    report_vec_mapper = ReportVecMapper()
    report_vec_mapper.insert_report_vec(report_id, report_vec, report_vec_file_path)
    print( "cal report {} 's sim_vec".format(report_id) )

def save_totally_same_report_vec( report_id, report_vec_file_path ):
    '''
    随便写的值，就记为0.5吧
    :param report_id:
    :param report_vec_file_path:
    :return:
    '''
    report_vec = [0.5,0.5]
    report_vec_mapper = ReportVecMapper()
    report_vec_mapper.insert_report_vec(report_id, report_vec, report_vec_file_path)

if __name__ == "__main__":
    procedures_1_text = "负责利用train loader进行训练 负责利用train loader进行训练"
    procedures_2_text = "负责利用train loader进行训练 负责利用train loader进行训练"
    print(sentence_sim(word2vec_model, procedures_1_text, procedures_2_text))