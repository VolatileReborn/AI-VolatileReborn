# coding:utf-8
import numpy as np
import re


# remove english punctuation
def clean_str(string):
    string = re.sub(r"[^A-Za-z0-9(),!?\'\`]", " ", string)
    string = re.sub(r"\'s", " \'s", string)
    string = re.sub(r"\'ve", " \'ve", string)
    string = re.sub(r"n\'t", " n\'t", string)
    string = re.sub(r"\'re", " \'re", string)
    string = re.sub(r"\'d", " \'d", string)
    string = re.sub(r"\'ll", " \'ll", string)
    string = re.sub(r",", " , ", string)
    string = re.sub(r"!", " ! ", string)
    string = re.sub(r"\(", " \( ", string)
    string = re.sub(r"\)", " \) ", string)
    string = re.sub(r"\?", " \? ", string)
    string = re.sub(r"\s{2,}", " ", string)
    return string.strip().lower()


# load and label the data
# label 0 represent bug descriptions
# label 1 represent reproduction steps
def load_data_and_labels(procedure_data_file, problem_data_file):
    procedure_examples = list(open(procedure_data_file, "r", encoding="utf-8").readlines())
    procedure_examples = [s.strip() for s in procedure_examples]
    problem_examples = list(open(problem_data_file, "r", encoding="utf-8").readlines())
    problem_examples = [s.strip() for s in problem_examples]
    x_text = procedure_examples + problem_examples

    x_text = [sent for sent in x_text]
    positive_labels = [[0, 1] for _ in procedure_examples]
    negative_labels = [[1, 0] for _ in problem_examples]
    y = np.concatenate([positive_labels, negative_labels], 0)
    return [x_text, y]


# get the data of one batch
def batch_iter(data, batch_size, num_epochs, shuffle=True):
    data = np.array(data)
    data_size = len(data)
    num_batches_per_epoch = int((len(data)-1)/batch_size) + 1
    for epoch in range(num_epochs):
        # mess up the order of data
        if shuffle:
            # Randomly generate an out-of-order array as the subscript of the data set array
            shuffle_indices = np.random.permutation(np.arange(data_size))
            shuffled_data = data[shuffle_indices]
        else:
            shuffled_data = data
        # divide batches
        for batch_num in range(num_batches_per_epoch):
            start_index = batch_num * batch_size
            end_index = min((batch_num + 1) * batch_size, data_size)
            yield shuffled_data[start_index:end_index]


if __name__ == '__main__':
    procedure_data_file = 'segment/procedure.txt'
    problem_data_file = 'segment/problem.txt'
    load_data_and_labels(procedure_data_file, problem_data_file)








