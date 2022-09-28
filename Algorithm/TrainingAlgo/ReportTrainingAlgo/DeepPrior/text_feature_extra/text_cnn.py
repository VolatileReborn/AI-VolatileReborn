# import tensorflow as tf
#
#
# class TextCNN(object):
#     """
#     sequence_length: The length of the sentence. fill all the sentences to the same length
#     num_classes: The numbers of categories of the output layer
#     vocab_size: Vocabulary size
#                 The shape of embedding layer is [vocabulary_size, embedding_size]。
#     embedding_size: The dimension of embedding。
#     filter_sizes: The number of words covered by convolutional filters
#     num_filters: The number of filters for each filter size
#     l2_reg_lambda
#     """
#
#     def __init__(self, sequence_length, num_classes, vocab_size,
#                  embedding_size, filter_sizes, num_filters, l2_reg_lambda=0.0):
#         # Define placeholders. The number of neurons kept in the dropout layer is also the input of the network,
#         # because we can only enable dropout during training, but not when evaluating the model。
#         self.input_x = tf.placeholder(tf.int32, [None, sequence_length], name="input_x")
#         self.input_y = tf.placeholder(tf.float32, [None, num_classes], name="input_y")
#         self.dropout_keep_prob = tf.placeholder(tf.float32, name="dropout_keep_prob")
#
#         # define constant，Keeping track of l2 regularization loss (optional)
#         l2_loss = tf.constant(0.0)
#         # Embedding layer
#         with tf.device('/cpu:0'), tf.name_scope("embedding"):
#             self.W = tf.Variable(
#                 # Map the word index of the vocabulary to a low-dimensional vector representation
#                 tf.random_uniform([vocab_size, embedding_size], -1.0, 1.0), name="W")
#             # Embedding operation
#             self.embedded_chars = tf.nn.embedding_lookup(self.W, self.input_x)
#             self.embedded_chars_expanded = tf.expand_dims(self.embedded_chars, -1)
#
#         # Create a convolution + maxpool layer for each filter size
#         pooled_outputs = []
#         for i, filter_size in enumerate(filter_sizes):
#             with tf.name_scope("conv-maxpool-%s" % filter_size):
#                 # convolutional layer
#                 filter_shape = [filter_size, embedding_size, 1, num_filters]
#                 W = tf.Variable(tf.truncated_normal(filter_shape, stddev=0.1), name="W")
#                 b = tf.Variable(tf.constant(0.1, shape=[num_filters]), name="b")
#                 conv = tf.nn.conv2d(
#                     self.embedded_chars_expanded,
#                     W,
#                     strides=[1, 1, 1, 1],
#                     padding="VALID",
#                     name="conv")
#                 # nonlinear activation
#                 h = tf.nn.relu(tf.nn.bias_add(conv, b), name="relu")
#                 # max pooling
#                 pooled = tf.nn.max_pool(
#                     h,
#                     ksize=[1, sequence_length - filter_size + 1, 1, 1],
#                     strides=[1, 1, 1, 1],
#                     padding='VALID',
#                     name="pool")
#                 pooled_outputs.append(pooled)
#
#         # Combine all the pooled features
#         num_filters_total = num_filters * len(filter_sizes)
#         self.h_pool = tf.concat(pooled_outputs, 3)
#         self.h_pool_flat = tf.reshape(self.h_pool, [-1, num_filters_total])
#         # Add dropout
#         with tf.name_scope("dropout"):
#             self.h_drop = tf.nn.dropout(self.h_pool_flat, self.dropout_keep_prob)
#
#         with tf.name_scope("output"):
#             W = tf.get_variable(
#                 "W",
#                 shape=[num_filters_total, num_classes],
#                 initializer=tf.contrib.layers.xavier_initializer())
#             b = tf.Variable(tf.constant(0.1, shape=[num_classes]), name="b")
#             l2_loss += tf.nn.l2_loss(W)
#             l2_loss += tf.nn.l2_loss(b)
#             self.scores = tf.nn.xw_plus_b(self.h_drop, W, b, name="scores")
#             self.predictions = tf.argmax(self.scores, 1, name="predictions")
#
#         # Loss
#         with tf.name_scope("loss"):
#             losses = tf.nn.softmax_cross_entropy_with_logits(logits=self.scores, labels=self.input_y)
#             self.loss = tf.reduce_mean(losses) + l2_reg_lambda * l2_loss
#
#         # Accuracy
#         with tf.name_scope("accuracy"):
#             correct_predictions = tf.equal(self.predictions, tf.argmax(self.input_y, 1))
#             self.accuracy = tf.reduce_mean(tf.cast(correct_predictions, "float"), name="accuracy")
