# 导包
import cv2 as cv
import numpy as np


# 获取车牌区域的字符拆分后的候选字符列表
# 参数：车牌候选区域（某一个）， candidate_plate_image
# 返回值：切分车牌字符，按顺序生成的车牌字符候选列表
def get_candidate_chars(candidate_plate_image):
    # 1. 图片预处理：灰度+二值化
    gray_image = cv.cvtColor(candidate_plate_image, cv.COLOR_BGR2GRAY)
    is_success, binary_image = cv.threshold(gray_image, 0, 255, cv.THRESH_OTSU)

    # 2. 向内缩进，去除外边框
    # 经验值
    offset_X = 4
    offset_Y = 8
    # 切片提取内嵌的区域
    offset_region = binary_image[offset_Y:-offset_Y, offset_X:-offset_X]
    # 生成工作区域
    working_region = offset_region

    # 3. 对汉字区域进行等值线找区域
    # 经验值：汉字区域占整体的1/8
    chinese_char_max_width = working_region.shape[1] // 10
    # 提取汉字区域
    chinese_char_region = working_region[:, 0:chinese_char_max_width]
    # 对汉字区域进行模糊处理
    cv.GaussianBlur(chinese_char_region, (9, 9), 0, dst=chinese_char_region)
    # 对整个区域找轮廓==等值线
    char_contours, _ = cv.findContours(working_region, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    cv.drawContours(candidate_plate_image, char_contours, -1, (0, 0, 255))

    # 4. 过滤不合适的轮廓（等值线框）
    # 经验值
    CHAR_MIN_WIDTH = working_region.shape[1] // 40
    CHAR_MIN_HEIGHT = working_region.shape[0] * 7 // 10
    CHAR_MAX_WIDTH = working_region.shape[1] // 4

    # 5. 逐个遍历所有候选的字符区域轮廓==等值线框，按照大小进行过滤
    valid_char_regions = []
    for i in np.arange(len(char_contours)):
        x, y, w, h = cv.boundingRect(char_contours[i])
        if CHAR_MAX_WIDTH >= w >= CHAR_MIN_WIDTH and h >= CHAR_MIN_HEIGHT:
            # 将字符区域的中心的x的坐标 和 字符区域 作为一个元组放入 valid_char_region 列表
            valid_char_regions.append((x, offset_region[y:y + h, x:x + w]))

    # 6. 按照区域的x坐标进行排序，并返回字符制表
    sorted_regions = sorted(valid_char_regions, key=lambda region: region[0])
    candidate_char_images = []
    for i in np.arange(len(sorted_regions)):
        candidate_char_images.append(sorted_regions[i][1])

    return candidate_char_images
