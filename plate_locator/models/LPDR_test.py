import os
from collections import Counter
from models import plate_locator as pl, detect as dt
import cv2 as cv
import numpy as np
from models.ocr_explorer import Explorer


# 图片文件测试
def picture_plate(image):
    plate_image = cv.imread(image)
    plate_image = cv.resize(plate_image, (156, 61))
    candidate_plates = pl.get_candidate_plates(plate_image)
    result = []
    for i in np.arange(len(candidate_plates)):
        cv.imshow('', candidate_plates[i])
        cv.waitKey()
        cv.destroyAllWindows()
        ocr_exp = Explorer()
        plate_str = ocr_exp(candidate_plates[i])
        result.append(plate_str)
    # 计数

    if len(result):
        collection_words = Counter(result)
        # 返回出现频率最大的字符串
        result_plate = collection_words.most_common(1)[0][0]
        return result_plate
    else:
        return


def plate(images):
    # 用于保留识别结果(str)
    result = []
    # 逐一读取图片识别车牌
    for i in np.arange(len(images)):

        candidate_result = picture_plate(images[i])
        if candidate_result is not None:
            result.append(candidate_result)
        #
    # 计数
    if len(result):
        collection_words = Counter(result)
        # 返回出现频率最大的字符串
        result_plate = collection_words.most_common(1)[0][0]
        return result_plate
    else:
        return

def test(filename):
    file = filename
    file_path = 'data/images/ccpd/' + file
    save_dir = 'runs/detect/exp'
    plate_file_path = 'runs/detect/exp/crops/plate'
    if os.path.isdir(save_dir) and os.path.isdir(os.path.join(save_dir, 'crops')) and os.path.isdir(os.path.join(save_dir, 'crops/plate')):
        file_lis = os.listdir(os.path.join(save_dir, 'crops/plate'))
        for file_name in file_lis:
            tf = os.path.join(save_dir, 'crops/plate', file_name)
            if not os.path.isdir(tf):
                os.remove(tf)
    opt = dt.parse_opt(file_path)
    dt.main(opt)
    images = []
    for root, dirs, files in os.walk(plate_file_path):
        for file in files:
            if file.endswith('jpg') or file.endswith('jpeg') or file.endswith('gif') or file.endswith(
                    'png') or file.endswith('bmp'):
                images.append(os.path.join(root, file))
    return plate(images)

if __name__ == '__main__':
    file = 'image2.jpg'
    file_path = '../data/images/ccpd/' + file
    save_dir = '../runs/detect/exp'
    plate_file_path = '../runs/detect/exp/crops/plate'
    if os.path.isdir(save_dir) and os.path.isdir(os.path.join(save_dir, 'crops')) and os.path.isdir(os.path.join(save_dir, 'crops/plate')):
        file_lis = os.listdir(os.path.join(save_dir, 'crops/plate'))
        for file_name in file_lis:
            tf = os.path.join(save_dir, 'crops/plate', file_name)
            if not os.path.isdir(tf):
                os.remove(tf)
    opt = dt.parse_opt(file_path)
    dt.main(opt)
    images = []
    for root, dirs, files in os.walk(plate_file_path):
        for file in files:
            if file.endswith('jpg') or file.endswith('jpeg') or file.endswith('gif') or file.endswith(
                    'png') or file.endswith('bmp'):
                images.append(os.path.join(root, file))
    print(plate(images))
