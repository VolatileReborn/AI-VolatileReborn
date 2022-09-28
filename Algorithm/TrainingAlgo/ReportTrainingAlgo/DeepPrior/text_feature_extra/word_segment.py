import jieba
import sys
import os

sys.path.append("../../../../SimilarityAlgo/")


def load_stopword_list(filepath):
    """
    create stop word list
    filepath : stop word file path

    """
    stopwords = [line.strip() for line in open(filepath, 'r', encoding='utf-8').readlines()]
    return stopwords


# perform word segment and record the result to file
def word_segment2file(readfile, outfile):
    for line in readfile.readlines():
        newline = jieba.cut(line, cut_all=False)
        outstr_list = list()
        for word in newline:
            outstr_list.append(word)
        str_out = ' '.join(outstr_list)
        print(str_out, file=outfile, end=' ')


# perform word segment and return word token list
def word_segment2token(sample):
    result = jieba.cut(sample, cut_all=False)
    outstr_list = list()
    curpath = os.path.dirname(os.path.realpath(__file__))
    stopwords = load_stopword_list(os.path.join(curpath, 'segment', 'stop_words.txt'))
    for word in result:
        if word not in stopwords:
            outstr_list.append(word)
    str_out = ' '.join(outstr_list)
    return str_out


if __name__ == '__main__':
    fromdir = "./data/"
    todir = "./segment/"
    stopWordFile = "stop_words.txt"
    # file = "problem.txt"
    file = "procedure.txt"
    infile = open(os.path.join(fromdir, file), 'r', encoding='UTF-8')
    outfile = open(os.path.join(todir, file), 'w+', encoding='UTF-8')
    # load stop word list
    stopwords = [line.strip() for line in open(os.path.join(todir, stopWordFile), 'r', encoding='UTF-8').readlines()]
    word_segment2file(infile, outfile)
    infile.close()
    outfile.close()
