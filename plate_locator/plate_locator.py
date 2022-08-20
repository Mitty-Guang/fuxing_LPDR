import util
import cv2 as cv
import numpy as np

# 借助 hsv + sobel算子 完成车牌区域的提取
# 参数：车牌（含有车牌的车辆）图片
# 返回值： 所有可能的车牌候选区域 = list
def get_candidate_plates_by_both(plate_image):
    # 1. 对含有车牌的车辆图片进行预处理
    preprocess_image = util.preprocess_plate_image_by_both(plate_image)
    # 2. 提取所有的等值线|车牌轮廓（可能）的区域
    contours, _ = cv.findContours(preprocess_image, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    # 3. 判断并获取所有的车牌区域的候选区域列表
    candidate_plates = []
    # 遍历所有的可能的车牌轮廓|等值线框
    for i in np.arange(len(contours)):
        # 逐一获取某一个可能的车牌轮廓区域
        contour = contours[i]
        # 根据面积、长宽比判断是否是候选的车牌区域
        if util.verify_plate_sizes(contour):
            # 完成旋转
            output_image = util.rotate_plate_image(contour, plate_image)
            # 统一尺寸
            uniformed_image = util.unify_plate_image(output_image)
            # 追加到车牌候选区域中
            candidate_plates.append(uniformed_image)
    # 返回含有所有的可能车牌区域的候选区域列表
    return candidate_plates