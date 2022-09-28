import csv

null_report = -1


def similarity(report1, report2, file_path):
    file = list(csv.reader(open(file_path, 'r')))
    return float(file[file[0].index(str(report1))][file[0].index(str(report2))])


def min_prior(path):
    pool = [null_report]
    query = list(csv.reader(open(path, 'r')))[0][2:]
    target = None
    while len(query) != 0:
        sim1 = 2
        sim2 = 2
        for q in query:
            for report in pool:
                sim = similarity(q, report, path)
                if sim < sim2:
                    sim2 = sim
                else:
                    continue
            if sim2 < sim1:
                target = q
                sim1 = sim2
            else:
                continue
        if null_report in pool:
            pool.remove(null_report)
        pool.append(target)
        query.remove(target)
        print('{}/{}'.format(len(pool), len(query)))
    print(pool)
    return pool


def avg_prior(path):
    pool = [null_report]
    query = list(csv.reader(open(path, 'r')))[0][2:]
    target = None
    while len(query) != 0:
        sim = 2
        for q in query:
            avg = sum([similarity(q, report, path) for report in pool]) / len(pool)
            if avg < sim:
                target = q
                sim = avg
        if null_report in pool:
            pool.remove(null_report)
        pool.append(target)
        query.remove(target)
    print(pool)
    return pool


def prioritize(path, strategy='MIN'):
    '''
    # 返回的是字符串形式的report_id列表
    :param path:
    :param strategy:
    :return:
    '''
    if strategy == 'MIN':
        return min_prior(path)
    if strategy == 'AVG':
        return avg_prior(path)
    else:
        return None
