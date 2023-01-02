from Algorithm.SimilarityAlgo.SimpleTextSimilarity import TextSimilarity
import Algorithm.TrainingAlgo.ReportTrainingAlgo.DeepPrior.ocr_baidu as ocr
from urllib.request import urlretrieve
import os

# current dir
curPath = os.path.dirname(os.path.realpath(__file__))


class SimpleEva(object):

    def report_evaluation(self, text, img_path_list):
        '''
        计算文本和图片的相似度
        '''

        img_dir_path = os.path.join(curPath, 'img')
        if not os.path.exists(img_dir_path):
            os.mkdir(img_dir_path)

        # download screenshots of the report ( implied by 'index' ) and return the local image path
        def download_img(image_url, index):
            tmp = image_url.split('.')
            extention_name = tmp[len(tmp) - 1]

            img_dir_path = os.path.join(curPath, 'img')
            path = os.path.join(img_dir_path,'img_' + str(index) + '.' + extention_name)
            urlretrieve(image_url, path)
            print("download img to {}".format(path))
            return path

        # 将所有图片下载到本地，img_path是所有报告的图片路径的list。 由于每篇报告只有一张图片，所以img_path的长度就是报告数
        local_img_path_list = []
        for i in range(len(img_path_list)):
            local_img_path_list.append(download_img(img_path_list[i], i))


        img_path = local_img_path_list[0]#为了性能， 只计算第一张图片
        ocr_res = ocr.get_baidu_ocr_res(img_path)

        text_sim = 0
        ocr_res_str = ''.join(ocr_res)
        if ocr_res_str == '' or text == '': #文字内容为空， 或者图片中没有文字， 此时评分为0
            text_sim = 0
        else:
            text_sim = TextSimilarity.lcs(text, ocr_res_str)

        # for ocr_txt in ocr_res:
        #     # cal sim between two types text info
        #
        #
        #     if text_sim > 0.0001:
        #         break
        return text_sim

