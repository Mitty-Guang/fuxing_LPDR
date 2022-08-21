# coding=utf-8
# pylint: disable=C0111,too-many-arguments,too-many-instance-attributes,too-many-locals,redefined-outer-name,fixme
# pylint: disable=superfluous-parens, no-member, invalid-name

import sys

# import range
# from numpy.core.tests.test_mem_overlap import range

sys.path.insert(0, "../../python")
import mxnet as mx
import logging
import genPlate as gen


class OCRBatch(object):
    def __init__(self, data_names, data, label_names, label):
        self.data = data
        self.label = label
        self.data_names = data_names
        self.label_names = label_names

    @property
    def provide_data(self):
        return [(n, x.shape) for n, x in zip(self.data_names, self.data)]

    @property
    def provide_label(self):
        return [(n, x.shape) for n, x in zip(self.label_names, self.label)]


def rand_range(lo, hi):
    return lo + gen.r(hi - lo)


def gen_rand():
    name = ""
    label = []
    label.append(rand_range(0, 31))
    label.append(rand_range(41, 65))
    for i in range(5):
        label.append(rand_range(31, 65))

    name += gen.chars[label[0]]
    name += gen.chars[label[1]]
    for i in range(5):
        name += gen.chars[label[i + 2]]
    return name, label


def gen_sample(genplate, width, height):
    num, label = gen_rand()
    img = genplate.generate(num)
    img = gen.cv2.resize(img, (width, height))
    img = gen.np.multiply(img, 1 / 255.0)
    img = img.transpose(2, 0, 1)
    return label, img


class OCRIter(mx.io.DataIter):
    def __init__(self, count, batch_size, num_label, height, width):
        """

        :param count: 训练数量
        :param batch_size: 分多少批次
        :param num_label:
        :param height:
        :param width:
        """
        super(OCRIter, self).__init__()
        self.genplate = gen.GenPlate("./font/platech.ttf", './font/platechar.ttf', './NoPlates')
        self.batch_size = batch_size
        self.count = count
        self.height = height
        self.width = width
        self.provide_data = [('data', (batch_size, 3, height, width))]
        self.provide_label = [('softmax_label', (batch_size, num_label))]
        print("start")

    def __iter__(self):

        for k in range((int)(self.count / self.batch_size)):
            data = []
            labels = []
            for i in range(self.batch_size):
                label, img = gen_sample(self.genplate, self.width, self.height)
                data.append(img)
                labels.append(label)
                # print("批次：%d，序号：%d，数据迭代：%s" % (k, i, label))

            data_all = [mx.nd.array(data)]
            label_all = [mx.nd.array(labels)]
            data_names = ['data']
            label_names = ['softmax_label']
            data_batch = OCRBatch(data_names, data_all, label_names, label_all)
            yield data_batch

    def reset(self):
        pass


def get_ocrnet():
    data = mx.symbol.Variable('data')
    label = mx.symbol.Variable('softmax_label')
    conv1 = mx.symbol.Convolution(data=data, kernel=(5, 5), num_filter=32)
    pool1 = mx.symbol.Pooling(data=conv1, pool_type="max", kernel=(2, 2), stride=(1, 1))
    relu1 = mx.symbol.Activation(data=pool1, act_type="relu")

    conv2 = mx.symbol.Convolution(data=relu1, kernel=(5, 5), num_filter=32)
    pool2 = mx.symbol.Pooling(data=conv2, pool_type="avg", kernel=(2, 2), stride=(1, 1))
    relu2 = mx.symbol.Activation(data=pool2, act_type="relu")

    conv3 = mx.symbol.Convolution(data=relu2, kernel=(3, 3), num_filter=32)
    pool3 = mx.symbol.Pooling(data=conv3, pool_type="avg", kernel=(2, 2), stride=(1, 1))
    relu3 = mx.symbol.Activation(data=pool3, act_type="relu")

    conv4 = mx.symbol.Convolution(data=relu3, kernel=(3, 3), num_filter=32)
    pool4 = mx.symbol.Pooling(data=conv4, pool_type="avg", kernel=(2, 2), stride=(1, 1))
    relu4 = mx.symbol.Activation(data=pool4, act_type="relu")

    flatten = mx.symbol.Flatten(data=relu2)
    fc1 = mx.symbol.FullyConnected(data=flatten, num_hidden=120)
    fc21_dropout = mx.symbol.Dropout(fc1, p=0.5)
    fc21 = mx.symbol.FullyConnected(data=fc21_dropout, num_hidden=65)

    fc22_dropout = mx.symbol.Dropout(fc1, p=0.5)
    fc22 = mx.symbol.FullyConnected(data=fc22_dropout, num_hidden=65)

    fc23_dropout = mx.symbol.Dropout(fc1, p=0.5)
    fc23 = mx.symbol.FullyConnected(data=fc23_dropout, num_hidden=65)

    fc24_dropout = mx.symbol.Dropout(fc1, p=0.5)
    fc24 = mx.symbol.FullyConnected(data=fc24_dropout, num_hidden=65)

    fc25_dropout = mx.symbol.Dropout(fc1, p=0.5)
    fc25 = mx.symbol.FullyConnected(data=fc25_dropout, num_hidden=65)

    fc26_dropout = mx.symbol.Dropout(fc1, p=0.5)
    fc26 = mx.symbol.FullyConnected(data=fc26_dropout, num_hidden=65)

    fc27_dropout = mx.symbol.Dropout(fc1, p=0.5)
    fc27 = mx.symbol.FullyConnected(data=fc27_dropout, num_hidden=65)

    fc2 = mx.symbol.Concat(*[fc21, fc22, fc23, fc24, fc25, fc26, fc27], dim=0)
    label = mx.symbol.transpose(data=label)
    label = mx.symbol.Reshape(data=label, target_shape=(0,))
    return mx.symbol.SoftmaxOutput(data=fc2, label=label, name="softmax")


def Accuracy(label, pred):
    label = label.T.reshape((-1,))
    hit = 0
    total = 0
    for i in range(int(pred.shape[0] / 7)):
        ok = True
        for j in range(7):
            k = i * 7 + j
            if gen.np.argmax(pred[k]) != int(label[k]):
                ok = False
                break
        if ok:
            hit += 1
        total += 1
    return 1.0 * hit / total


def train(trainSize, testSize, cnnTrainPrefix, batch_size):
    """
    训练
    :param trainSize: 训练数量
    :param testSize:
    :param cnnTrainPrefix:
    :param batch_size:
    :return:
    """
    devs = [mx.cpu(i) for i in range(2)]
    network = get_ocrnet()
    model = mx.model.FeedForward(
        ctx=devs,
        symbol=network,
        num_epoch=1,
        learning_rate=0.001,
        wd=0.00001,
        initializer=mx.init.Xavier(factor_type="in", magnitude=2.34),
        momentum=0.9)
    data_train = OCRIter(trainSize, batch_size, 7, 30, 120)
    data_test = OCRIter(testSize, batch_size, 7, 30, 120)
    head = '%(asctime)-15s %(message)s'
    logging.basicConfig(level=logging.DEBUG, format=head)
    model.fit(X=data_train, eval_data=data_test, eval_metric=Accuracy,
              batch_end_callback=mx.callback.Speedometer(batch_size, 50))
    model.save(cnnTrainPrefix, 1)
    print("end")


import sys
import time

if __name__ == '__main__':
    trainSize = 1000
    testSize = 100
    cnnTrainPrefix = './tmp/trainCNN/cnn-ocr-model'
    try:
        trainSize = int(sys.argv[1])
        testSize = int(sys.argv[2])
        cnnTrainPrefix = sys.argv[3]
    except BaseException as be:
        print(be.__str__())
        time.sleep(5)
    batch_size = 8
    train(trainSize, testSize, cnnTrainPrefix, batch_size)
