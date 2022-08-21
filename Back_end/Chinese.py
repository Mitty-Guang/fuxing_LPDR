import os
import numpy as np
import cv2 as cv
import tensorflow._api.v2.compat.v1 as tf

tf.disable_v2_behavior()

MODEL_PATH = "model/Chinese/chinese"
TRAIN_DIR = "data/chs_train"
TEST_DIR = "data/chs_test"
# 中文图片重置的宽、高
IMAGE_WIDTH = 20
IMAGE_HEIGHT = 20
CLASSIFICATION_COUNT = 31
LABEL_DICT = {
    'chuan': 0, 'e': 1, 'gan': 2, 'gan1': 3, 'gui': 4, 'gui1': 5, 'hei': 6, 'hu': 7, 'ji': 8, 'jin': 9,
    'jing': 10, 'jl': 11, 'liao': 12, 'lu': 13, 'meng': 14, 'min': 15, 'ning': 16, 'qing': 17, 'qiong': 18, 'shan': 19,
    'su': 20, 'sx': 21, 'wan': 22, 'xiang': 23, 'xin': 24, 'yu': 25, 'yu1': 26, 'yue': 27, 'yun': 28, 'zang': 29,
    'zhe': 30
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
                data.append(resized_image.ravel())
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


# 设置权重，并根据shape，使用截断正态分布获取随机数进行初始化
def weight_variable(shape):
    initial = tf.truncated_normal(shape, stddev=0.1)
    return tf.Variable(initial)


# 设置偏置，并初始化
def bias_variable(shape):
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial)


# 设置卷积层
def conv2d(x, W):
    return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')


# 设置池化层
def max_pool_2x2(x):
    return tf.nn.max_pool(x, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')


x = tf.placeholder(tf.float32, shape=[None, IMAGE_HEIGHT * IMAGE_WIDTH])

y_ = tf.placeholder(tf.float32, shape=[None, CLASSIFICATION_COUNT])

x_image = tf.reshape(x, [-1, IMAGE_HEIGHT, IMAGE_WIDTH, 1])

W_conv1 = weight_variable([5, 5, 1, 32])  # color channel == 1; 32 filters

b_conv1 = bias_variable([32])

h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1)  # 20x20

h_pool1 = max_pool_2x2(h_conv1)  # 20x20 => 10x10

W_conv2 = weight_variable([5, 5, 32, 64])
b_conv2 = bias_variable([64])
h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)  # 10x10
h_pool2 = max_pool_2x2(h_conv2)  # 10x10 => 5x5

W_fc1 = weight_variable([5 * 5 * 64, 1024])  # 全连接第一个隐藏层神经元1024个

b_fc1 = bias_variable([1024])

h_pool2_flat = tf.reshape(h_pool2, [-1, 5 * 5 * 64])  # 转成-1列

h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)  # Affine+ReLU

keep_prob = tf.placeholder(tf.float32)  # 定义Dropout的比例
h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)  # 执行dropout

W_fc2 = weight_variable([1024, CLASSIFICATION_COUNT])  # 全连接输出为 CLASSIFICATION_COUNT 个

b_fc2 = bias_variable([CLASSIFICATION_COUNT])

y_conv = tf.matmul(h_fc1_drop, W_fc2) + b_fc2

learning_rate = 5 * 1e-5  # 学习率
max_epochs = 50  # 代数
batch_size = 100  # 批大小
check_step = 10  # 检查点步长

logits = y_conv
y = tf.nn.softmax(logits=logits)
cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(y), axis=1))

train_step = tf.train.AdamOptimizer(learning_rate).minimize(cross_entropy)

correct_prediction = tf.equal(tf.argmax(y_conv, 1), tf.argmax(y_, 1))
# 计算准确率，转化为浮点数，求平均（数组）
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

# 开始训练
with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())

    print("装载训练数据...")
    # 获取训练集的特征矩阵、标签向量
    train_data, train_labels = load_data(TRAIN_DIR)
    # 对训练集的特征矩阵进行正则化
    train_data = normalize_data(train_data)
    # 对训练集的标签向量执行独热编码
    train_labels = onehot_labels(train_labels)
    # 探查训练集
    print("装载%d条数据，每条数据%d个特征" % (train_data.shape))

    # 获取训练集的总样本数
    train_samples_count = len(train_data)
    train_indicies = np.arange(train_samples_count)
    # 获得打乱的索引序列
    np.random.shuffle(train_indicies)

    print("装载测试数据...")
    # 获取测试集的特征矩阵、标签向量
    test_data, test_labels = load_data(TEST_DIR)
    # 对测试集的特征矩阵进行同样（同训练集）的正则化
    test_data = normalize_data(test_data)
    # 对测试集的标签向量执行独热编码
    test_labels = onehot_labels(test_labels)
    # 探查测试集
    print("装载%d条数据，每条数据%d个特征" % (test_data.shape))

    # 天花板取整（np.ceil），获取迭代次数（此处，就是批次）
    iters = int(np.ceil(train_samples_count / batch_size))
    print("Training...")
    # 逐个 epoch 进行训练
    for epoch in range(1, max_epochs + 1):
        print("Epoch #", epoch)
        # 逐个批次进行迭代-训练
        for i in range(1, iters + 1):
            # 获取本批数据
            # 获取本批数据的起点位置
            start_idx = (i * batch_size) % train_samples_count
            # 获取本批数据的起点、终点范围 = 批次范围
            idx = train_indicies[start_idx: start_idx + batch_size]
            # 按本批次范围获取训练集的特征矩阵
            batch_x = train_data[idx, :]
            # 按本批次范围获取训练集的标签向量
            batch_y = train_labels[idx, :]
            # 开始训练：
            _, batch_accuracy = sess.run([train_step, accuracy], feed_dict={x: batch_x, y_: batch_y, keep_prob: 0.5})
            # 判断检查点，输出中间结果
            if i % check_step == 0:
                print("Iter:", i, "of", iters, "batch_accuracy=", batch_accuracy)
    print("Training completed.")

    # 保存模型
    print("Saving model...")
    saver = tf.train.Saver()
    saved_file = saver.save(sess, MODEL_PATH)
    print('Model saved to ', saved_file)

    test_accuracy = accuracy.eval(feed_dict={x: test_data, y_: test_labels, keep_prob: 1.0})
    print('Test accuracy %g' % test_accuracy)
