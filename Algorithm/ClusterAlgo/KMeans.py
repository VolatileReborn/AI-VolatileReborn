from sklearn.cluster import KMeans
import numpy as np
import  csv

# 构造数据样本点集X，并计算K-means聚类
file_path = "/Users/lyk/Projects/Volatile/ai-volatile/Data/ReportVectors/task1-report-vecs.csv"
class KMeansStrategy():

    def cluster(self, report_vec_file_path):
        '''
        返回值：

        :param report_vec_file_path:
        :return: [ { "report_id": 10,"coordinate": [0.23, 0.87],"cluster_id": 19 }, ... ]
        '''
        with open(report_vec_file_path, 'r') as csvfile:
            reader = csv.reader(csvfile)
            header = next(reader) # 跳过矩阵头

            report_id_list = []
            data = []
            for line in reader:
                report_id_list.append(int(line[0])) # report_id

                line = line[1:]  # 去除第一个元素（report_id）
                ele_float_list = []
                for ele_str in line:
                    ele_float_list.append(float(ele_str))  # 将元素从str转成float
                data.append(ele_float_list)

            print(header)
            print(data)

        X = np.array(data)

        # 簇数量，默认是3
        n_clusters = self.__adjust_cluster_num(3, len(data))

        kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(X)

        # 输出及聚类后的每个样本点的标签（即类别），预测新的样本点所属类别
        label_list = kmeans.labels_
        label_list = label_list.tolist() # 将np.array类型转化为list类型，使其元素可以序列化

        print(kmeans.labels_)
        print(kmeans.predict([[0, 0], [4, 4], [2, 1]]))

        res_list = []
        for i in range(len(report_id_list)):
            item = {}
            item["report_id"] = report_id_list[i]
            item["coordinate"] = [ data[i][0], data[i][1] ]
            item["cluster_id"] = label_list[i]
            # print(type(label_list[i]))
            res_list.append(item)
        print(res_list)

        return res_list

    def __adjust_cluster_num(self, n_clusters, point_num):
        '''
        调整聚类的簇数量，使其不大于样本点的个数
        :param n_clusters:
        :param point_num:
        :return:
        '''
        if n_clusters > point_num:
            n_clusters = point_num
        return n_clusters




if __name__ == "__main__":
    clusterAlgo = KMeansStrategy()
    clusterAlgo.cluster(file_path)

