# -*- coding: utf-8 -*-
'''
识别主项的主类
'''

import os

import cv2
import numpy as np
import tensorflow as tf
from PIL import Image

import tf_model as model

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # 忽略烦人的警告
index = {"京": 0, "沪": 1, "津": 2, "渝": 3, "冀": 4, "晋": 5, "蒙": 6, "辽": 7, "吉": 8, "黑": 9, "苏": 10, "浙": 11, "皖": 12,
         "闽": 13, "赣": 14, "鲁": 15, "豫": 16, "鄂": 17, "湘": 18, "粤": 19, "桂": 20, "琼": 21, "川": 22, "贵": 23, "云": 24,
         "藏": 25, "陕": 26, "甘": 27, "青": 28, "宁": 29, "新": 30, "0": 31, "1": 32, "2": 33, "3": 34, "4": 35, "5": 36,
         "6": 37, "7": 38, "8": 39, "9": 40, "A": 41, "B": 42, "C": 43, "D": 44, "E": 45, "F": 46, "G": 47, "H": 48,
         "J": 49, "K": 50, "L": 51, "M": 52, "N": 53, "P": 54, "Q": 55, "R": 56, "S": 57, "T": 58, "U": 59, "V": 60,
         "W": 61, "X": 62, "Y": 63, "Z": 64};

chars = ["京", "沪", "津", "渝", "冀", "晋", "蒙", "辽", "吉", "黑", "苏", "浙", "皖", "闽", "赣", "鲁", "豫", "鄂", "湘", "粤", "桂",
         "琼", "川", "贵", "云", "藏", "陕", "甘", "青", "宁", "新", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A",
         "B", "C", "D", "E", "F", "G", "H", "J", "K", "L", "M", "N", "P", "Q", "R", "S", "T", "U", "V", "W", "X",
         "Y", "Z"
         ];
'''
Test one image against the saved models and parameters
'''


def get_random_image(test_dir='./tmp/'):
    '''
    随机获取图片
    Return: ndarry
    '''
    test_image = []
    for file in os.listdir(test_dir):
        test_image.append(test_dir + file)
    test_image = list(test_image)
    n = len(test_image)
    ind = np.random.randint(0, n)
    img_dir = test_image[ind]
    return get_image(img_dir)


def get_image(img_dir='./tmp/plate/00.jpg'):
    '''
    获取指定的图片
    Return: ndarry
    '''
    print("imgFile %s" % (img_dir))
    image_show = Image.open(img_dir)

    print("imgData: %s" % (image_show))
    # plt.imshow(image_show)
    image = cv2.imread(img_dir)
    img = np.multiply(image, 1 / 255.0)
    image = np.array([img])
    print("image.shape:", image.shape)
    return image


def handler(img_dir=None, logs_train_dir=None):
    '''
    识别图片的主控制类
    :param img_dir: 图片路径
    :return:
    '''
    image_array = None
    if img_dir is not None:
        # 获取指定的图片
        image_array = get_image(img_dir=img_dir)
    else:
        # 随机获取图片
        image_array = get_random_image(test_dir='./tmp/plate/')
    line = sb(image_array, logs_train_dir)
    print("识别图片的结果为：" + line)
    return line


def sb(image_array, logs_train_dir='./tmp/train_logs_50000/'):
    '''
    识别图片
    :return:
    '''
    batch_size = 1
    x = tf.placeholder(tf.float32, [batch_size, 72, 272, 3])
    keep_prob = tf.placeholder(tf.float32)

    # logit = model.inference(x,keep_prob)
    logit1, logit2, logit3, logit4, logit5, logit6, logit7 = model.inference(x, keep_prob)

    # logit1 = tf.nn.softmax(logit1)
    # logit2 = tf.nn.softmax(logit2)
    # logit3 = tf.nn.softmax(logit3)
    # logit4 = tf.nn.softmax(logit4)
    # logit5 = tf.nn.softmax(logit5)
    # logit6 = tf.nn.softmax(logit6)
    # logit7 = tf.nn.softmax(logit7)

    saver = tf.train.Saver()

    with tf.Session() as sess:
        print("Reading checkpoint...")
        print("logs_train_dir:" + logs_train_dir)
        ckpt = tf.train.get_checkpoint_state(logs_train_dir)
        if ckpt and ckpt.model_checkpoint_path:
            global_step = ckpt.model_checkpoint_path.split('/')[-1].split('-')[-1]
            saver.restore(sess, ckpt.model_checkpoint_path)
            print('Loading success, global_step is %s' % global_step)
        else:
            print('No checkpoint file found')

        pre1, pre2, pre3, pre4, pre5, pre6, pre7 = sess.run([logit1, logit2, logit3, logit4, logit5, logit6, logit7],
                                                            feed_dict={x: image_array, keep_prob: 1.0})
        prediction = np.reshape(np.array([pre1, pre2, pre3, pre4, pre5, pre6, pre7]), [-1, 65])
        # prediction = np.array([[pre1],[pre2],[pre3],[pre4],[pre5],[pre6],[pre7]])
        # print(prediction)

        max_index = np.argmax(prediction, axis=1)
        print('max_index %s' % (max_index))
        line = ''
        for i in range(prediction.shape[0]):
            if i == 0:
                result = np.argmax(prediction[i][0:31])
            if i == 1:
                result = np.argmax(prediction[i][41:65]) + 41
            if i > 1:
                result = np.argmax(prediction[i][31:65]) + 31

            line += chars[result] + " "
        print('predicted: ' + line)
        return line


import sys
import time

if __name__ == "__main__":
    # img_dir = './tmp/plate/00.jpg'
    img_dir = None
    logs_train_dir = './tmp/train_logs_50000/'
    try:
        img_dir = sys.argv[1]
        logs_train_dir = sys.argv[2]
    except BaseException as be:
        print(be.__str__())
        time.sleep(5)
    handler(img_dir=img_dir, logs_train_dir=logs_train_dir)
