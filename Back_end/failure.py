import os
import numpy as np
import cv2 as cv
import tensorflow as tf

MODEL_PATH = "model/English/english"
TRAIN_DIR = "data/enu_train"
TEST_DIR = "data/enu_test"
# 英文图片重置的宽、高
IMAGE_WIDTH = 20
IMAGE_HEIGHT = 20
CLASSIFICATION_COUNT = 34
LABEL_DICT = {
    '0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
    'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15, 'G': 16, 'H': 17, 'J': 18, 'K': 19,
    'L': 20, 'M': 21, 'N': 22, 'P': 23, 'Q': 24, 'R': 25, 'S': 26, 'T': 27, 'U': 28, 'V': 29,
    'W': 30, 'X': 31, 'Y': 32, 'Z': 33
}

# 设置GPU内存为陆续分配，防止一次性的全部分配GPU内存，导致系统过载
physical_devices = tf.config.list_physical_devices('GPU')
try:
    tf.config.experimental.set_memory_growth(physical_devices[0], True)
except:
    # Invalid device or cannot modify virtual devices once initialized.
    pass


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
                data.append(resized_image)
                labels.append(LABEL_DICT[item])

    return np.array(data), np.array(labels)


# 本质：完成数据的正则化
def normalize_data(data):
    return (data - data.mean()) / data.max()


# 构建 独热编码
def onehot_labels(labels):
    onehots = np.zeros((len(labels), CLASSIFICATION_COUNT))
    for i in np.arange(len(labels)):
        onehots[i, labels[i]] = 1
    return onehots


learning_rate = 1e-4  # 学习率
max_epochs = 40  # 代数
batch_size = 50  # 批大小
check_step = 10  # 检查点步长

model = tf.keras.Sequential([
    tf.keras.layers.Conv2D(16, (3, 3), activation='relu', input_shape=[20, 20, 1]),
    tf.keras.layers.MaxPooling2D(),
    tf.keras.layers.Conv2D(32, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D(),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(120, activation='relu'),
    tf.keras.layers.Dense(84, activation='relu'),
    tf.keras.layers.Dense(34, activation='softmax')
])

model.summary()

model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate),
    loss=tf.keras.losses.sparse_categorical_crossentropy,
    metrics=[tf.keras.metrics.sparse_categorical_crossentropy]
)

train_data, train_labels = load_data(TRAIN_DIR)
# 对训练集的特征矩阵进行正则化
train_data = normalize_data(train_data)
# 对训练集的标签向量执行独热编码
train_labels = onehot_labels(train_labels)

train_data = tf.convert_to_tensor(train_data)
train_labels = tf.convert_to_tensor(train_labels)
train_dataset = tf.data.Dataset.from_tensor_slices((train_data, train_labels))
model.fit(train_dataset, epochs=max_epochs)
