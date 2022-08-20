# 工具类
# 完成导包
import cv2 as cv
import numpy as np

# 0 预处理车牌（含有车牌）图片 hsv + sobel
# 参数：车辆（含有车牌）图片，plate_image
# 返回值：预处理后的车牌图片，preprocess_image
def preprocess_plate_image_by_both(plate_image):
    # hsv
    # 1. 将一张 RGB 图片转换为 HSV 图片格式
    hsv_image = cv.cvtColor(plate_image, cv.COLOR_BGR2HSV)
    # 获取h、s、v图片分量，图片shape
    h_split, s_split, v_split = cv.split(hsv_image)
    rows, cols = h_split.shape
    # 2. 遍历图片，找出蓝色区域
    # 创建全黑背景，== 原始图片大小
    binary_image = np.zeros((rows, cols), dtype=np.uint8)
    # 设置感兴趣|提取的 颜色的 hsv 的区间：可调的经验值
    HSV_MIN_BLUE_H = 100
    HSV_MAX_BLUE_H = 140
    HSV_MIN_BLUE_SV = 75
    HSV_MAX_BLUE_SV = 255

    # 遍历图片的每一个像素,找到满足条件（hsv找蓝色）的像素点，设置为255 ==binary_image中
    for row in np.arange(rows):
        for col in np.arange(cols):
            H = h_split[row, col]
            S = s_split[row, col]
            V = v_split[row, col]
            # 判断像素落在蓝色区域并满足 sv 条件
            if (HSV_MIN_BLUE_H < H < HSV_MAX_BLUE_H) and (HSV_MIN_BLUE_SV < S < HSV_MAX_BLUE_SV) and (
                    HSV_MIN_BLUE_SV < V < HSV_MAX_BLUE_SV):
                binary_image[row, col] = 255

    # sobel 算子
    # 高斯模糊
    blured_image = cv.GaussianBlur(plate_image, (5, 5), 0)
    # 转成灰度图
    gray_image = cv.cvtColor(blured_image, cv.COLOR_BGR2GRAY)
    # 使用Sobel算子，求水平方向一阶导数
    # 使用 cv.CV_16S
    grad_x = cv.Sobel(gray_image, cv.CV_16S, 1, 0, ksize=3)
    grad_y = cv.Sobel(gray_image, cv.CV_16S, 0, 1, ksize=3)
    # 转成 CV-_8U - 借助 cv.convertScaleAbs()方法
    abs_grad_x = cv.convertScaleAbs(grad_x)
    abs_grad_y = cv.convertScaleAbs(grad_y)
    # 叠加水平和垂直方向，获取 sobel 的输出
    gray_image = cv.addWeighted(abs_grad_x, 1, abs_grad_y, 0, 0)
    new_blured_image = cv.GaussianBlur(gray_image, (5, 5), 0)
    # 二值化操作
    is_success, threshold_image = cv.threshold(new_blured_image, 0, 255, cv.THRESH_OTSU)

    # 执行闭操作=>车牌连成矩形区域
    final_image = np.zeros((rows, cols), dtype=np.uint8)
    for row in np.arange(rows):
        for col in np.arange(cols):
            if threshold_image[row, col] == 255 and binary_image[row, col] == 255:
                final_image[row, col] = 255
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (10, 3))
    morphology_image = cv.morphologyEx(final_image, cv.MORPH_CLOSE, kernel)
    return morphology_image

# 1. 判断是否是车牌区域（依据：面积、长宽比）
# 参数：某个轮廓-候选车牌区域： contour
# 返回值：bool（True/False）
def verify_plate_sizes(contour):
    # 声明常量：长宽比（最小、最大），面积（最小、最大） == 可以微调
    MIN_ASPECT_RATIO = 2.0
    MAX_ASPECT_RATIO = 4.0
    MIN_AREA = 34.0 * 8 * 10
    MAX_AREA = 34.0 * 8 * 100

    # 获取矩形特征描述的等值线区域，返回：中心点坐标、长和宽、旋转角度--float
    (center_x, center_y), (w, h), angle = cv.minAreaRect(contour)
    # 获取宽、高=>int
    w = int(w)
    h = int(h)

    # 进行面积判断
    area = w * h
    if area > MAX_AREA or area < MIN_AREA:
        return False

    # 进行长宽比的判断
    # 获取长宽比
    aspect_ratio = w / h
    # 判定车盘是否竖排
    if aspect_ratio < 1:
        aspect_ratio = 1.0 / aspect_ratio
    # 判定
    if aspect_ratio > MAX_ASPECT_RATIO or aspect_ratio < MIN_ASPECT_RATIO:
        return False

    return True

# 2. 车牌的旋转矫正（依据：根据长宽判断旋转角度是否需要修正、借助转换|旋转矩阵和原始的图片|扩充图片完成旋转|仿射）
# 参数：车牌区域：contour， 原始图片|车牌旋转态图片：plate_image
# 返回值： output_image == 完成旋转矫正后的车牌图片
def rotate_plate_image(contour, plate_image):
    # 获取车牌区域正交的外接矩形，同时也会返回 长、宽
    # boundingRect 用于获取与 等值线框（轮廓框）contour 的四个角点正交的矩形
    # 返回 左上的坐标（x, y），宽（w）、高（h）
    x, y, w, h = cv.boundingRect(contour)
    # 生成该外接正交矩形的图片矩阵：对原始车牌图牌的切片提取
    bounding_image = plate_image[y:y+h, x:x+w]

    # *1. 判断并修订旋转角度
    # 获取矩形特征描述的等值线区域，返回：中心点坐标、长和宽、旋转角度
    rect = cv.minAreaRect(contour)
    # 获取整数形式的 长、宽
    rect_width, rect_height = np.int0(rect[1])
    # 获取旋转角度|畸变角度
    angle = np.abs(rect[2])
    # 自行调整：1. 大小关系 2. 角度修订
    if rect_width > rect_height:
        temp = rect_width
        rect_width = rect_height
        rect_height = temp
        angle = 90 + angle  # 需要理解&修改
    # 对于较小的旋转角度，不予理会，具体值：需要微调的经验值
    if angle <= 5.0 or angle >= 175:
        # 直接返回包含车牌区域的车牌图片，不旋转
        return bounding_image

    # 完成旋转
    # 创建一个放大的图片区域， 保存旋转之后的结果
    enlarged_width = w * 3 // 2
    enlarged_height = h * 3 // 2
    enlarged_image = np.zeros((enlarged_height, enlarged_width, plate_image.shape[2]), dtype=plate_image.dtype)

    x_in_enlarged = (enlarged_width - w) // 2
    y_in_enlarged = (enlarged_height - h) // 2
    # 获取放大图片的居中图片（全0）
    roi_image = enlarged_image[y_in_enlarged:y_in_enlarged + h, x_in_enlarged:x_in_enlarged + w, :]
    # 将旋转前的图片（bounding_image）放置到放大图片的居中位置 == copy
    cv.addWeighted(roi_image, 0, bounding_image, 1, 0, roi_image)
    # 计算旋转中心：就是放大图片的中心
    new_center = (enlarged_width // 2, enlarged_height // 2)
    # *2. 开始旋转
    # 计算获取旋转的转换矩阵，旋转角度需要自行微调
    transform_matrix = cv.getRotationMatrix2D(new_center, angle + 270, 1.0)
    # 进行|完成旋转：原始图片和旋转转换矩阵的仿射计算
    transform_image = cv.warpAffine(enlarged_image, transform_matrix, (enlarged_width, enlarged_height))

    # 获取输出图：截取与最初的等值线框|车牌轮廓的长宽相同的部分
    output_image = cv.getRectSubPix(transform_image, (rect_height, rect_width), new_center)

    return output_image

# 3. 统一尺寸：将车牌图片调整到统一一致的大小
# 参数：需要统一尺寸的车牌： plate_image
# 返回值： resize 之后的统一尺寸的图片： uniformed_image
def unify_plate_image(plate_image):
    # 声明统一的尺寸
    PLATE_STD_HEIGHT = 36
    PLATE_STD_WIDTH = 136
    # 完成 resize
    uniformed_image = cv.resize(plate_image, (PLATE_STD_WIDTH, PLATE_STD_HEIGHT))
    return uniformed_image
