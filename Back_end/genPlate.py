# coding=utf-8
import os
from math import *

import cv2 as cv2
import numpy as np
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

# font = ImageFont.truetype("Arial-Bold.ttf",14)

index = {"京": 0, "沪": 1, "津": 2, "渝": 3, "冀": 4, "晋": 5, "蒙": 6, "辽": 7, "吉": 8, "黑": 9, "苏": 10, "浙": 11, "皖": 12,
         "闽": 13, "赣": 14, "鲁": 15, "豫": 16, "鄂": 17, "湘": 18, "粤": 19, "桂": 20, "琼": 21, "川": 22, "贵": 23, "云": 24,
         "藏": 25, "陕": 26, "甘": 27, "青": 28, "宁": 29, "新": 30, "0": 31, "1": 32, "2": 33, "3": 34, "4": 35, "5": 36,
         "6": 37, "7": 38, "8": 39, "9": 40, "A": 41, "B": 42, "C": 43, "D": 44, "E": 45, "F": 46, "G": 47, "H": 48,
         "J": 49, "K": 50, "L": 51, "M": 52, "N": 53, "P": 54, "Q": 55, "R": 56, "S": 57, "T": 58, "U": 59, "V": 60,
         "W": 61, "X": 62, "Y": 63, "Z": 64}
# 所有车牌字符
chars = ["京", "沪", "津", "渝", "冀", "晋", "蒙", "辽", "吉", "黑", "苏", "浙", "皖", "闽", "赣", "鲁", "豫", "鄂", "湘", "粤", "桂",
         "琼", "川", "贵", "云", "藏", "陕", "甘", "青", "宁", "新", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A",
         "B", "C", "D", "E", "F", "G", "H", "J", "K", "L", "M", "N", "P", "Q", "R", "S", "T", "U", "V", "W", "X",
         "Y", "Z"
         ]


def genPlateString(pos, val):
    """
    生成车牌号
    :param pos:
    :param val:
    :return:
    """
    plateStr = ""
    box = [0, 0, 0, 0, 0, 0, 0]
    if (pos != -1):
        box[pos] = 1
    for unit, cpos in zip(box, range(len(box))):
        if unit == 1:
            plateStr += val
        else:
            if cpos == 0:
                plateStr += chars[r(31)]
            elif cpos == 1:
                plateStr += chars[41 + r(24)]
            else:
                if int(np.random.random()*5) >= 1:
                    plateStr += chars[31 + r(10)]
                else:
                    plateStr += chars[41 + r(24)]

    return plateStr


def tfactor(img):
    """
    添加饱和度光照的噪声
    :param img:
    :return:
    """
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    hsv[:, :, 0] = hsv[:, :, 0] * (0.8 + np.random.random() * 0.2)
    hsv[:, :, 1] = hsv[:, :, 1] * (0.3 + np.random.random() * 0.7)
    hsv[:, :, 2] = hsv[:, :, 2] * (0.2 + np.random.random() * 0.8)

    img = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    return img



def GenCh(f, val):
    """
    生成中文字符
    :param f:
    :param val:
    :return:
    """
    img = Image.new("RGB", (45, 70), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    draw.text((0, 3), val, (0, 0, 0), font=f)
    img = img.resize((23, 70))
    A = np.array(img)

    return A


def GenCh1(f, val):
    """
    生成英文字符
    :param f:
    :param val:
    :return:
    """
    img = Image.new("RGB", (23, 70), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    draw.text((0, 2), val.encode('utf-8').decode('utf-8'), (0, 0, 0), font=f)
    A = np.array(img)
    return A


def r(val):
    return int(np.random.random() * val)

class GenPlate:

    def __init__(self, fontCh, fontEng, NoPlates):
        self.fontC = ImageFont.truetype(fontCh, 43, 0)
        self.fontE = ImageFont.truetype(fontEng, 60, 0)
        self.img = np.array(Image.new("RGB", (226, 70), (255, 255, 255)))
        self.bg = cv2.resize(cv2.imread("./images/template.bmp"), (226, 70))
        self.smu = cv2.imread("./images/smu2.jpg")
        self.noplates_path = []
        for parent, parent_folder, filenames in os.walk(NoPlates):
            for filename in filenames:
                path = parent + "/" + filename
                self.noplates_path.append(path)

    def draw(self, val):
        offset = 2

        self.img[0:70, offset + 8:offset + 8 + 23] = GenCh(self.fontC, val[0])
        self.img[0:70, offset + 8 + 23 + 6:offset + 8 + 23 + 6 + 23] = GenCh1(self.fontE, val[1])
        for i in range(5):
            base = offset + 8 + 23 + 6 + 23 + 17 + i * 23 + i * 6
            self.img[0:70, base: base + 23] = GenCh1(self.fontE, val[i + 2])
        return self.img

    def generate(self, text):
        """
        根据车牌号生成图片
        :param text:
        :return:
        """
        if len(text) == 7:
            fg = self.draw(text.encode('utf-8').decode(encoding="utf-8"))
            fg = cv2.bitwise_not(fg)
            com = cv2.bitwise_or(fg, self.bg)

            com = tfactor(com)

            return com

    # 将生成的车牌图片写入文件夹，对应的label写入label.txt
    def genBatch(self, batchSize, labelFile, outputPath, size=(272, 72)):
        """
        批量生成
        :param batchSize:
        :param labelFile:
        :param outputPath:
        :param size:
        :return:
        """
        if (not os.path.exists(outputPath)):
            os.mkdir(outputPath)
        outfile = open(labelFile, 'w', encoding="utf-8")
        for i in range(batchSize):
            plateStr = genPlateString(-1, -1)
            # utf-8 一个汉字占三个字节
            print(plateStr)
            # 生成图片
            img = self.generate(plateStr)
            img = cv2.resize(img, size)
            # 写文件
            cv2.imwrite(outputPath + "/" + str(i).zfill(2) + ".jpg", img)
            # 写入label文件中
            outfile.write(plateStr + "\n")


import sys
import time

if __name__ == '__main__':
    batchSize = 50000  # 生成图片数
    outputPath = './tmp/plate'
    labelFile = './tmp/label.txt'
    try:
        batchSize = int(sys.argv[1])
        outputPath = sys.argv[2]
    except BaseException as be:
        print(be.__str__())
        time.sleep(5)

    print("batchSize:%d,outputPath:%s" % (batchSize, outputPath))
    # new对象
    genPlate = GenPlate("./font/platech.ttf", './font/platechar.ttf', "./NoPlates")
    genPlate.genBatch(batchSize=batchSize, labelFile=labelFile,
                      outputPath=outputPath,
                      size=(272, 72))
