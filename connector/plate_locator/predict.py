import cv2 as cv
import numpy as np
import joblib


def normalize_data(data):
    return (data - data.mean()) / data.max()


def load_image(image, width, height):
    resized_image = cv.resize(image, (width, height))
    normalized_image = normalize_data(resized_image)
    data = []
    data.append(normalized_image.ravel())
    return np.array(data)


ENGLISH_LABELS = [
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K',
    'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
    'W', 'X', 'Y', 'Z']

CHINESE_LABELS = [
    "川", "鄂", "赣", "甘", "贵", "桂", "黑", "沪", "冀", "津",
    "京", "吉", "辽", "鲁", "蒙", "闽", "宁", "青", "琼", "陕",
    "苏", "晋", "皖", "湘", "新", "豫", "渝", "粤", "云", "藏",
    "浙"]

ENGLISH_MODEL_PATH = "models/mlp_enu.m"
CHINESE_MODEL_PATH = "models/chinese.m"
ENGLISH_IMAGE_WIDTH = 20
ENGLISH_IMAGE_HEIGHT = 20
CHINESE_IMAGE_WIDTH = 24
CHINESE_IMAGE_HEIGHT = 48
english_model = joblib.load(ENGLISH_MODEL_PATH)
chinese_model = joblib.load(CHINESE_MODEL_PATH)


def predict_chinese_chars(image):
    chinese_image = load_image(image, CHINESE_IMAGE_WIDTH, CHINESE_IMAGE_HEIGHT)
    predict = chinese_model.predict(chinese_image)
    return CHINESE_LABELS[predict[0]]


def predict_english_chars(image):
    english_image = load_image(image, ENGLISH_IMAGE_WIDTH, ENGLISH_IMAGE_HEIGHT)
    predict = english_model.predict(english_image)
    return ENGLISH_LABELS[predict[0]]