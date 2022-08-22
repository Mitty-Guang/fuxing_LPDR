import os
import numpy as np
import cv2 as cv
from sklearn import svm
import joblib

MODEL_PATH = "model/English/english.m"
TRAIN_DIR = "data/enu_train"
TEST_DIR = "data/enu_test"
IMAGE_WIDTH = 20
IMAGE_HEIGHT = 20
CLASSIFICATION_COUNT = 34  # 数字+英文字符共有34种类别
LABEL_DICT = {
    '0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
    'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15, 'G': 16, 'H': 17, 'J': 18, 'K': 19,
    'L': 20, 'M': 21, 'N': 22, 'P': 23, 'Q': 24, 'R': 25, 'S': 26, 'T': 27, 'U': 28, 'V': 29,
    'W': 30, 'X': 31, 'Y': 32, 'Z': 33
}


def load_data(dir_path):
    data = []
    labels = []

    for item in os.listdir(dir_path):
        item_path = os.path.join(dir_path, item)
        if os.path.isdir(item_path):
            for subitem in os.listdir(item_path):
                subitem_path = os.path.join(item_path, subitem)
                gray_image = cv.imread(subitem_path, cv.IMREAD_GRAYSCALE)
                resized_image = cv.resize(gray_image, (IMAGE_WIDTH, IMAGE_HEIGHT))
                data.append(resized_image.ravel())
                labels.append(LABEL_DICT[item])

    return np.array(data), np.array(labels)


def normalize_data(data):
    return (data - data.mean()) / data.max()


def train():
    print("装载训练数据...")
    train_data, train_labels = load_data(TRAIN_DIR)
    normalized_data = normalize_data(train_data)
    print("装载%d条数据，每条数据%d个特征" % (normalized_data.shape))

    print("训练中...")
    model = svm.SVC(decision_function_shape='ovo')  # ovo代表采用1 vs 1的方式进行多类别分类处理
    model.fit(normalized_data, train_labels)

    print("训练完成，保存模型...")
    joblib.dump(model, MODEL_PATH)
    print("模型保存到:", MODEL_PATH)


def test():
    print("装载测试数据...")
    test_data, test_labels = load_data(TEST_DIR)
    normalized_data = normalize_data(test_data)
    print("装载%d条数据，每条数据%d个特征" % (normalized_data.shape))

    print("装载模型...")
    model = joblib.load(MODEL_PATH)
    print("模型装载完毕，开始测试...")
    predicts = model.predict(normalized_data)
    errors = np.count_nonzero(predicts - test_labels)
    print("测试完毕，预测正确：%d 条，预测错误:%d 条， 正确率：%f" %
          (len(predicts) - errors, errors, (len(predicts) - errors) / len(predicts)))


train()
test()
