import numpy as np
import jieba
import os
import gensim


def cal_dis(model, s1, s2):
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
                v += model[word]
            except:
                length -= 1
        if length == 0:
            return np.zeros(size)
        v /= length
        return v

    def eucli_distance(A, B):
        return round(np.sqrt(sum(np.power((A - B), 2))), 4)

    v1, v2 = sentence_vector(s1), sentence_vector(s2)
    dis = eucli_distance(v1, v2)
    return dis


def get_min_cost_step(cost_a, cost_b, step_a, step_b):
    min_cost = 0
    min_step = 0
    if cost_a < cost_b:
        min_cost = cost_a
        min_step = step_a
    elif cost_a == cost_b:
        min_cost = cost_a
        min_step = min(step_a, step_b)
    else:
        min_cost = cost_b
        min_step = step_b
    return min_cost, min_step


def dtw_distance(ts_a, ts_b, min_dis, max_dis, isOneValue=False, mww=10000):
    def format_dis(dis, min, max):
        if min == 0. and max == 0.:
            return dis
        else:
            tmp_dis = (dis - min) / (max - min)
            return round(tmp_dis, 4)

    max_dtw_dis = 0.0
    min_dtw_dis = 100000000000000

    # Create cost matrix via broadcasting with large int
    ts_a, ts_b = np.array(ts_a), np.array(ts_b)
    M, N = len(ts_a), len(ts_b)
    cost = np.zeros((M, N))
    step = np.zeros((M, N))

    curpath = os.path.dirname(os.path.realpath(__file__))
    word2vec_model = gensim.models.Word2Vec.load(os.path.join(curpath, 'bugdata_format_model_100'))

    # Initialize the first row and column
    dis = cal_dis(word2vec_model, ts_a[0], ts_b[0])
    cost[0, 0] = format_dis(dis, min_dis, max_dis)
    if dis > max_dtw_dis:
        max_dtw_dis = dis
    if dis < min_dtw_dis:
        min_dtw_dis = dis
    step[0, 0] = 1
    for i in range(1, M):
        dis = cal_dis(word2vec_model, ts_a[i], ts_b[0])
        cost[i, 0] = cost[i - 1, 0] + format_dis(dis, min_dis, max_dis)
        step[i, 0] = i + 1
        if dis > max_dtw_dis:
            max_dtw_dis = dis
        if dis < min_dtw_dis:
            min_dtw_dis = dis

    for j in range(1, N):
        dis = cal_dis(word2vec_model, ts_a[0], ts_b[j])
        cost[0, j] = cost[0, j - 1] + format_dis(dis, min_dis, max_dis)
        step[0, j] = j + 1
        if dis > max_dtw_dis:
            max_dtw_dis = dis
        if dis < min_dtw_dis:
            min_dtw_dis = dis

    # Populate rest of cost matrix within window
    for i in range(1, M):
        for j in range(1, N):
            tmp_cost, tmp_step = get_min_cost_step(cost[i - 1, j - 1], cost[i, j - 1], step[i - 1, j - 1],
                                                   step[i, j - 1])
            min_cost, min_step = get_min_cost_step(tmp_cost, cost[i - 1, j], tmp_step, step[i - 1, j])
            dis = cal_dis(word2vec_model, ts_a[i], ts_b[j])
            cost[i, j] = min_cost + format_dis(dis, min_dis, max_dis)
            step[i, j] = min_step + 1
            if dis > max_dtw_dis:
                max_dtw_dis = dis
            if dis < min_dtw_dis:
                min_dtw_dis = dis

    # Return DTW distance given window
    if max_dis == 0. and min_dis == 0. and isOneValue == False:
        return round(min_dtw_dis, 4), (round(max_dtw_dis + 1, 4))
    else:
        return round(cost[-1, -1] / step[-1, -1], 4)
