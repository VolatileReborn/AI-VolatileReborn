import re

#  text_feature对象:  {'procedures_list': procedures, 'problem_widget': problem_widget, 'problems_list': problems}
def text_feature_extraction(descriptions, reproduction_steps):
    res = []
    for i in range(len(descriptions)):
        description = descriptions[i]
        reproduction_step = reproduction_steps[i]

        procedures = re.split('[,，.。.: ]', reproduction_step)
        problem_widget = description
        problems = re.split('[,，.。.: ]', description)

        dict_res = {'procedures_list': procedures, 'problem_widget': problem_widget, 'problems_list': problems}
        res.append(dict_res)

    return res
#
# import tensorflow as tf
# from text_feature_extra.word_segment import word_segment2token
# import numpy as np
# import os
# import re
# import text_feature_extra.data_helpers as data_helpers
# from tensorflow.contrib import learn
# import jieba.posseg
#
#
# # text_feature对象:  {'procedures_list': procedures, 'problem_widget': problem_widget, 'problems_list': problems}
# def text_feature_extraction(samples):
#     x_raw_list = []
#     sentences_list = []
#     for sample in samples:
#         sentences = re.split(' |。', sample)
#         sentences = [item for item in filter(lambda x: x != '', sentences)]
#         sentences_list.append(sentences)
#         x_raw = []
#         for sentence in sentences:
#             tmp = word_segment2token(sentence)
#             x_raw.append(tmp.strip())
#         x_raw_list.append(x_raw)
#
#     res = []
#
#     curpath = os.path.dirname(os.path.realpath(__file__))
#     tf.flags.DEFINE_string("checkpoint_dir", os.path.join(curpath, 'runs', 'TextCNN_model', 'checkpoints'),
#                            "Checkpoint directory from training run")
#     tf.flags.DEFINE_boolean("eval_train", False, "Evaluate on all training data")
#
#     # Misc Parameters
#     tf.flags.DEFINE_boolean("allow_soft_placement", True, "Allow device soft device placement")
#     tf.flags.DEFINE_boolean("log_device_placement", False, "Log placement of ops on devices")
#     FLAGS = tf.flags.FLAGS
#
#     # Map data into vocabulary
#     vocab_path = os.path.join(FLAGS.checkpoint_dir, "..", "vocab")
#     vocab_processor = learn.preprocessing.VocabularyProcessor.restore(vocab_path)
#     x_test_list = []
#     for x_raw in x_raw_list:
#         x_test = np.array(list(vocab_processor.transform(x_raw)))
#         x_test_list.append(x_test)
#
#     print("\nEvaluating...\n")
#
#     # Evaluation
#     # ==================================================
#     checkpoint_file = tf.train.latest_checkpoint(FLAGS.checkpoint_dir)
#     print("checkpoint_file========", checkpoint_file)
#
#     graph = tf.Graph()
#     with graph.as_default():
#         session_conf = tf.ConfigProto(
#             allow_soft_placement=FLAGS.allow_soft_placement,
#             log_device_placement=FLAGS.log_device_placement)
#         sess = tf.Session(config=session_conf)
#         with sess.as_default():
#             # Load the saved meta graph and restore variables
#             saver = tf.train.import_meta_graph("{}.meta".format(checkpoint_file))
#
#             saver.restore(sess, checkpoint_file)
#
#             # Get the placeholders from the graph by name
#             input_x = graph.get_operation_by_name("input_x").outputs[0]
#             # input_y = graph.get_operation_by_name("input_y").outputs[0]
#             dropout_keep_prob = graph.get_operation_by_name("dropout_keep_prob").outputs[0]
#
#             # Tensors we want to evaluate
#             predictions = graph.get_operation_by_name("output/predictions").outputs[0]
#
#             for j in range(len(x_test_list)):
#                 # Generate batches for one epoch
#                 batches = data_helpers.batch_iter(list(x_test_list[j]), 64, 1, shuffle=False)
#                 # model prediction result
#                 all_predictions = []
#                 for x_test_batch in batches:
#                     batch_predictions = sess.run(predictions, {input_x: x_test_batch, dropout_keep_prob: 1.0})
#                     all_predictions = np.concatenate([all_predictions, batch_predictions])
#
#                 problems = []
#                 procedures = []
#                 for i in range(len(all_predictions)):
#                     short_sentences = sentences_list[j]
#                     if all_predictions[i] == 0.0:
#                         # label = 0 represent bug descriptions
#                         problems.append(short_sentences[i])
#                     else:
#                         # label = 1 represent reproduction steps
#                         procedures.append(short_sentences[i])
#
#                 # lexical analysis
#                 problem_widget = ''
#                 last_procedure = ''
#                 if len(procedures) >= 1:
#                     last_procedure = procedures[len(procedures) - 1]
#                 last_procedure_seged = jieba.posseg.cut(last_procedure.strip())
#                 first_v = False
#                 for x in last_procedure_seged:
#                     if first_v:
#                         if x.flag != 'x' and x.flag != 'm':
#                             problem_widget += x.word
#                     else:
#                         if x.flag == 'v':
#                             first_v = True
#                 dict_res = {'procedures_list': procedures, 'problem_widget': problem_widget, 'problems_list': problems}
#                 res.append(dict_res)
#
#     return res
