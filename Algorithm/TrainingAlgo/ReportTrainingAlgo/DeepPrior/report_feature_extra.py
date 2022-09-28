import pandas as pd
import Algorithm.TrainingAlgo.ReportTrainingAlgo.DeepPrior.text_feature_extra.text_feature_extraction as tfe
import Algorithm.TrainingAlgo.ReportTrainingAlgo.DeepPrior.img_feature_extra.image_feature_extraction as ife
import Algorithm.TrainingAlgo.ReportTrainingAlgo.DeepPrior.ocr_baidu as ocr
import numpy as np
import jieba
import os
import gensim
import math
import csv
from urllib.request import urlretrieve
from Utils.SymbolHandler import ReportEnum

# sim threshold between text extracted by OCR from widget images and
# problem widget text analyzed by text_feature_extra module. (0.87 default)
thre = 0.7

# current dir
curPath = os.path.dirname(os.path.realpath(__file__))

model_path = os.path.join(curPath, 'text_feature_extra/bugdata_format_model_100')
# pre-trained word2vec model
word2vec_model = gensim.models.Word2Vec.load(
    model_path)  # 调用先前的word2vec模型


# cal text sim between text extracted by OCR from widget images
# and problem widget text analyzed by text_feature_extra module.
def widget_problem_text_sim(model, s1, s2):
    size = model.layer1_size

    # transform sentences into vectors
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
                v += model.wv[word]
            except:
                length -= 1
        if length == 0:
            return np.zeros(size)
        v /= length

        return v

    # cosine sim between two vectors
    def cos_sim(a, b):
        if len(a) != len(b):
            return None
        part_up = 0.0
        a_sq = 0.0
        b_sq = 0.0
        for a1, b1 in zip(a, b):
            part_up += a1 * b1
            a_sq += a1 ** 2
            b_sq += b1 ** 2
        part_down = math.sqrt(a_sq * b_sq)
        if part_down == 0.0:
            return 0
        else:
            return part_up / part_down

    v1, v2 = sentence_vector(s1), sentence_vector(s2)
    return cos_sim(v1, v2)


# find problem widget image from all widgets by problem_widget text info
# problem_widget: 缺陷的文字描述
def distinguish_widgets(widget_path_list, problem_widget):
    problem_widget_path = ''
    print('problem_widget={}'.format(problem_widget))
    for path in widget_path_list:
        # get text extracted by OCR from widget images
        ocr_res = ocr.get_baidu_ocr_res(path)
        print('path:{}'.format(path))
        for ocr_txt in ocr_res:
            # cal sim between two types text info
            similarity = widget_problem_text_sim(word2vec_model, ocr_txt, problem_widget)
            print('problem_widget:{},ocr_txt:{},similarity={}'.format(problem_widget, ocr_txt, similarity))
            # if the sim is higher than threshold, then the widget image will be recognized as problem widget
            if ocr_txt == problem_widget or similarity >= thre:
                problem_widget_path = path
                break
        if not problem_widget_path == '':
            break
    print('problem_widget:{},problem_widget_path:{}'.format(problem_widget, problem_widget_path))
    return problem_widget_path


# the main process of extract report feature
def extract_report_feature(file_path, tag):
    # read .csv file content
    # .csv内容为：
    # index     description     img_url
    # ***       ***             ***
    # 即每行是一个report， 每个report只有一张图片
    reports = pd.read_csv(file_path)
    report_ids = list(reports[ReportEnum.REPORT_ID])  # 报告id的列表
    descriptions = list(reports[ReportEnum.DEFECT_EXPLANATION])
    reproduction_steps = list(reports[ReportEnum.DEFECT_REPRODUCTION_STEP])
    images = list(reports[ReportEnum.DefectPictureEnum.IMG_URL])

    if not os.path.exists(os.path.join(curPath, 'img_feature_extra', 'Screenshots')):
        os.mkdir(os.path.join(curPath, 'img_feature_extra', 'Screenshots'))

    # download screenshots of the report ( implied by 'index' ) and return the local image path
    def download_img(image_url, index):
        tmp = image_url.split('.')
        path = os.path.join(curPath, 'img_feature_extra', 'Screenshots', str(index) + '.' + tmp[len(tmp) - 1])
        urlretrieve(image_url, path)
        print("download img to {}".format(path))
        return path

    # 将所有图片下载到本地，img_path是所有报告的图片路径的list。 由于每篇报告只有一张图片，所以img_path的长度就是报告数
    img_path_list = []
    for i in range(len(report_ids)):
        img_path_list.append(download_img(images[i], report_ids[i]))

    # extract text feature
    text_feature_list = tfe.text_feature_extraction(descriptions, reproduction_steps)
    print("-----------successfully extract text feature------------")
    # extract img feature
    img_feature_list = ife.image_feature_extraction(img_path_list)
    print("-----------successfully extract image feature-----------")

    # record widget categories info in .csv file
    print('-----------begin record widget_category-----------')
    widget_category_file = os.path.join(curPath, 'img_alz_res', 'widget_category', str(tag) + '.csv')

    c_file = open(widget_category_file, 'w', encoding='utf-8', newline='')
    csv_writer = csv.writer(c_file)
    csv_writer.writerow(['index', 'Button', 'CheckBox', 'CheckedTextView', 'EditText', 'ImageButton', 'ImageView',
                         'ProgressBar', 'ProgressBarHorizontal', 'ProgressBarVertical', 'RadioButton',
                         'RatingBar', 'SeekBar', 'Switch', 'Spinner', 'TextView'])
    widget_category_list = []
    for i in range(len(img_feature_list)):
        img_feature = img_feature_list[i]
        widget_category_vec = img_feature['compo_categories']
        widget_category_list.append(widget_category_vec)
        csv_writer.writerow([report_ids[i], widget_category_vec[0], widget_category_vec[1], widget_category_vec[2],
                             widget_category_vec[3], widget_category_vec[4], widget_category_vec[5],
                             widget_category_vec[6], widget_category_vec[7], widget_category_vec[8],
                             widget_category_vec[9], widget_category_vec[10], widget_category_vec[11],
                             widget_category_vec[12], widget_category_vec[13], widget_category_vec[14]])
    c_file.close()
    print('-----------finish record widget_category---------')

    print("-----------begin find problem widget and record---------")
    problem_widget_file = os.path.join(curPath, 'img_alz_res', 'problem_widget_path', str(tag) + '.csv')
    p_file = open(problem_widget_file, 'w', encoding='utf-8')
    csv_writer1 = csv.writer(p_file, lineterminator='\n')
    csv_writer1.writerow(['index', 'path'])
    problem_widget_path_list = []

    # 计算每个报告的problem widget, 方法是将该报告的图片（以地址的形式）和对bug的文字描述传入distinguish_widgets方法
    for i in range(len(img_path_list)):
        img_feature = img_feature_list[i]
        text_feature = text_feature_list[i]
        compo_paths = img_feature['compo_paths']
        # problem_widget对象是关于该problem_widget的text description
        problem_widget = text_feature['problem_widget']
        problem_widget_path = distinguish_widgets(compo_paths, problem_widget)
        problem_widget_path_list.append(problem_widget_path)
        csv_writer1.writerow([report_ids[i], problem_widget_path_list[i]])
    print("-----------finish find problem widget--------")
    return text_feature_list, widget_category_list, problem_widget_path_list


if __name__ == "__main__":
    similarity = widget_problem_text_sim(word2vec_model, "Word2Vec 模型的期望输入是进过分词的句子列表，即是某个二维数组。这里我们暂时使用 Python 内置的数组，不过其在输入数据集较大的情况下会占用大量的 RAM。Gensim 本身只是要求能够迭代的有序句子列表，因此在工程实践中我们可以使用自定义的生成器，只在内存中保存单条语句。", "Word2Vec 模型的期望输入是进过分词的句子列表，即是某个二维数组。这里我们暂时使用 Python 内置的数组，不过其在输入数据集较大的情况下会占用大量的 RAM。Gensim 本身只是要求能够迭代的有序句子列表，因此在工程实践中我们可以使用自定义的生成器，只在内存中保存单条语句。")
    print('similarity={}'.format(similarity))
