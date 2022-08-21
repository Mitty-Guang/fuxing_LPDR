# coding=utf-8
""" TestOne.py:对任意一张图片做识别预测
    输入:单张图片地址
    输出:单张图片的准确率
"""
__author__ = "szk"
__copyright__ = "Copyright (c) 2018 "
import cv2
import mxnet as mx
import numpy as np
import TestBatch as tb
import genPlate as gp


def TestRecognizeOne(labelName, plateImgFile, cnnOrcFilePrefix):
    """
    预测单张车牌图片的准确率
    :param plateImgFile:
    :param labelName:
    :param cnnOrcFilePrefix:
    :return:
    """
    plateImgFile = cv2.imread(plateImgFile)
    plateImgFile = cv2.resize(plateImgFile, (120, 30))
    cv2.imshow("img", plateImgFile)
    plateImgFile = np.swapaxes(plateImgFile, 0, 2)
    plateImgFile = np.swapaxes(plateImgFile, 1, 2)
    batch_size = 1
    _, arg_params, __ = mx.model.load_checkpoint(cnnOrcFilePrefix, 1)
    data_shape = [("data", (batch_size, 3, 30, 120))]
    input_shapes = dict(data_shape)
    sym = tb.getnet()
    executor = sym.simple_bind(ctx=mx.cpu(), **input_shapes)
    for key in executor.arg_dict.keys():
        if key in arg_params:
            arg_params[key].copyto(executor.arg_dict[key])
    executor.forward(is_train=True, data=mx.nd.array([plateImgFile]))
    probs = executor.outputs[0].asnumpy()
    line = ''
    for i in range(probs.shape[0]):
        if i == 0:
            result = np.argmax(probs[i][0:31])
        if i == 1:
            result = np.argmax(probs[i][41:65]) + 41
        if i > 1:
            result = np.argmax(probs[i][31:65]) + 31
        line += gp.chars[result]
    print('预测车牌号码为:' + line)
    print('实际车牌号码为:' + labelName)
    tb.Accuracy_pred(labelName, line)
    cv2.waitKey(0)
    return line


import sys
import time

if __name__ == '__main__':
    labelName = '苏B99999'
    plateImgFile = './tmp/plate/test.jpg'
    cnnOrcFilePrefix = './tmp/productCNN/cnn-ocr'
    try:
        labelName = sys.argv[1]
        plateImgFile = int(sys.argv[2])
        cnnOrcFilePrefix = sys.argv[3]
    except BaseException as be:
        print(be.__str__())
        time.sleep(5)
    # new对象
    print("labelName:%s, plateImgFile:%s, cnnOrcFilePrefix:%s" % (labelName, plateImgFile, cnnOrcFilePrefix))
    # 调用一张图片测试,输入参数为图片路径+名称,如:/Users/shelter/1.png
    TestRecognizeOne(labelName, plateImgFile, cnnOrcFilePrefix)
