# from keras.models import load_model
# import numpy as np
# import cv2
# import os
#
#
# class CNN:
#     def __init__(self, is_load=True):
#         self.data = None
#         self.model = None
#         self.image_shape = (64, 64, 3)
#         self.class_number = None
#         self.class_map = None
#         self.model_path = None
#         if is_load:
#             self.load()
#
#     def load(self):
#         curpath = os.path.dirname(os.path.realpath(__file__))
#         self.model_path = os.path.join(curpath, 'my_model.h5')
#         self.class_map = ['Button', 'CheckBox', 'CheckedTextView', 'EditText', 'ImageButton', 'ImageView',
#                           'NumberPicker', 'ProgressBar', 'ProgressBarHorizontal', 'ProgressBarVertical',
#                           'RadioButton', 'RatingBar', 'SeekBar', 'Switch', 'Spinner', 'TextView', 'ToggleButton']
#         self.image_shape = (64, 64, 3)
#         self.class_number = len(self.class_map)
#         self.model = load_model(self.model_path)
#         print('Model Loaded From', self.model_path)
#
#     def preprocess_img(self, image):
#         image = cv2.resize(image, self.image_shape[:2])
#         x = (image / 255).astype('float32')
#         x = np.array([x])
#         return x
#
#     def predict(self, imgs, compos, load=True, show=False):
#         if load:
#             self.load()
#         if self.model is None:
#             print(" No model loaded ")
#             return
#         for i in range(len(imgs)):
#             X = self.preprocess_img(imgs[i])
#             Y = self.class_map[np.argmax(self.model.predict(X))]
#             compos[i].category = Y
#             if show:
#                 print(Y)
#                 cv2.imshow('components', imgs[i])
#                 cv2.waitKey()
