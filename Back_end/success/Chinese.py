import cv2 as cv
import numpy as np
import os
# 导入 多次感知机的分类模型 MLPClassifier
from sklearn.neural_network import MLPClassifier
# 导入 完成模型持久化的 joblib
import joblib


# 初始配置
# 训练集、测试集位置
TRAIN_DIR = 'data/chs_train'
TEST_DIR = 'data/chs_test'
# 汉字图片宽、高
IMAGE_WIDTH = 24
IMAGE_HEIGHT = 48
# 给出类别数、类别-数值 字典
CLASSIFICATION_COUNT = 31
LABEL_DICT = {
    'chuan': 0, 'e': 1, 'gan': 2, 'gan1': 3, 'gui': 4, 'gui1': 5, 'hei': 6, 'hu': 7, 'ji': 8, 'jin': 9,
    'jing': 10, 'jl': 11, 'liao': 12, 'lu': 13, 'meng': 14, 'min': 15, 'ning': 16, 'qing': 17, 'qiong': 18, 'shan': 19,
    'su': 20, 'sx': 21, 'wan': 22, 'xiang': 23, 'xin': 24, 'yu': 25, 'yu1': 26, 'yue': 27, 'yun': 28, 'zang': 29,
    'zhe': 30
}
# 模型持久化的位置
MLP_ENU_MODEL_PATH = 'model/Chinese/chinese.m'


def load_data(dir_path):
    data = []
    labels = []
    # 获取数据集目录下的所有的子目录，并逐一遍历
    for item in os.listdir(dir_path):
        # 获取每一个具体样本类型的 os 的路径形式
        item_path = os.path.join(dir_path, item)
        # 判断只有目录，才进入进行下一级目录的遍历
        if os.path.isdir(item_path):
            # 到了每一个样本目录，遍历其下的每一个训练集样本文件-图片
            for subitem in os.listdir(item_path):
                subitem_path = os.path.join(item_path, subitem)
                gray_image = cv.imread(subitem_path, cv.IMREAD_GRAYSCALE)
                resized_image = cv.resize(gray_image, (IMAGE_WIDTH, IMAGE_HEIGHT))
                data.append(resized_image.ravel())
                labels.append(LABEL_DICT[item])
    # 分别赋值 样本数据特征、样本数据标签
    features = np.array(data)
    labels = np.array(labels)
    # 返回特征矩阵、标签向量
    return features, labels

def normalize_data(data):
    return (data - data.mean()) / data.max()


# 3. 训练 + 保存
def train():
    # 加载训练数据
    train_data, train_labels = load_data(TRAIN_DIR)
    # 数据的预处理
    normalized_data = normalize_data(train_data)

    # 模型创建
    model = MLPClassifier(hidden_layer_sizes=(48, 24), solver='lbfgs', alpha=1e-5, random_state=42)

    # 模型训练
    model.fit(normalized_data, train_labels)

    # 模型保存
    joblib.dump(model, MLP_ENU_MODEL_PATH)


# 4. 测试 + 评估
def test():
    test_data, test_labels = load_data(TEST_DIR)

    normalized_data = normalize_data(test_data)

    model = joblib.load(MLP_ENU_MODEL_PATH)

    predicts = model.predict(normalized_data)

    errors = np.count_nonzero(predicts - test_labels)
    print(errors)
    print((len(predicts) - errors) / len(predicts))


train()
test()
