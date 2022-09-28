import os
import cv2
import numpy as np
from random import randint as rint
from Algorithm.TrainingAlgo.ReportTrainingAlgo.DeepPrior.img_feature_extra.Config import Config
from matplotlib import pyplot as plt

C = Config()


def draw_bounding_box_class_plt(org, components, path, show=False):
    #Draw bounding box of components with their classes on the original image
    board = org.copy()
    b, g, r = cv2.split(board)
    srcImage_new = cv2.merge([r, g, b])
    fig, ax = plt.subplots(figsize=(11, 20))
    for compo in components:
        bbox = compo.put_bbox()
        ax.imshow(srcImage_new, aspect='equal')
        ax.add_patch(plt.Rectangle((bbox[0], bbox[1]), float(bbox[2] - bbox[0]), float(bbox[3] - bbox[1]),
                                   fill=False, edgecolor='blue', facecolor=None, linewidth=2))
        ax.text(bbox[0], bbox[1] - 2, '{:s}'.format(compo.category),
                bbox=dict(facecolor='blue', alpha=0.5),
                fontsize=8, color='white')

    plt.axis('off')
    plt.savefig(os.path.join(path, 'result.png'), bbox_inches='tight')
    if show:
        plt.show()


def draw_bounding_box_plt(org, components, color=(238, 216, 174), line=2, show=False, write_path=None, name='board'):
    #Draw bounding box of components on the original image
    board = org.copy()
    b, g, r = cv2.split(board)
    srcImage_new = cv2.merge([r, g, b])
    fig, ax = plt.subplots(figsize=(11, 20))
    for compo in components:
        bbox = compo.put_bbox()
        ax.imshow(srcImage_new, aspect='equal')
        ax.add_patch(plt.Rectangle((bbox[0], bbox[1]), float(bbox[2] - bbox[0]), float(bbox[3] - bbox[1]),
                                   fill=False, edgecolor='blue', facecolor=None, linewidth=2))
    plt.axis('off')
    if show:
        plt.show()

def draw_line(org, lines, color=(0, 255, 0), show=False):
    board = org.copy()
    line_h, line_v = lines
    for line in line_h:
        cv2.line(board, tuple(line['head']), tuple(line['end']), color, line['thickness'])
    for line in line_v:
        cv2.line(board, tuple(line['head']), tuple(line['end']), color, line['thickness'])
    if show:
        cv2.imshow('img', board)
        cv2.waitKey(0)
    return board


def draw_boundary(components, shape, show=False):
    board = np.zeros(shape[:2], dtype=np.uint8)  # binary board
    for component in components:
        # up and bottom: (column_index, min/max row border)
        for point in component.boundary[0] + component.boundary[1]:
            board[point[1], point[0]] = 255
        # left, right: (row_index, min/max column border)
        for point in component.boundary[2] + component.boundary[3]:
            board[point[0], point[1]] = 255
    if show:
        cv2.imshow('rec', board)
        cv2.waitKey(0)
    return board


def draw_region(region, broad, show=False):
    color = (rint(0,255), rint(0,255), rint(0,255))
    for point in region:
        broad[point[0], point[1]] = color

    if show:
        cv2.imshow('region', broad)
        cv2.waitKey()
    return broad


def draw_region_bin(region, broad, show=False):
    for point in region:
        broad[point[0], point[1]] = 255

    if show:
        cv2.imshow('region', broad)
        cv2.waitKey()
    return broad