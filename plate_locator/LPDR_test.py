import plate_locator as pl
import cv2 as cv
import numpy as np
import video_seperator as vs
from collections import Counter
import detect as dt

# 图片文件测试
def picture_plate(plate_image):
    height, width, _ = plate_image.shape
    plate_image = cv.resize(plate_image, (int(width*50/height), 50))
    candidate_plates = pl.get_candidate_plates_by_both(plate_image)
    for i in np.arange(len(candidate_plates)):
        cv.imshow('', candidate_plates[i])
        cv.waitKey()
        cv.destroyAllWindows()


# 视频文件测试
def video_plate(images):
    # 用于保留识别结果(str)
    result = []
    # 逐一读取图片识别车牌
    for i in np.arange(len(images)):
        candidate_result = picture_plate(images[i])
        result.append(candidate_result)
        #
    # 计数
    collection_words = Counter(result)
    # 返回出现频率最大的字符串
    result_plate, num = collection_words.most_common(1)
    return result_plate

if __name__ == '__main__':
    image = 'image4.jpg'
    image_path = 'data/images/ccpd/' + image
    plate_file_path = 'runs/detect/exp/crops/plate/' + image
    opt = dt.parse_opt(image_path)
    dt.main(opt)

    plate_image = cv.imread(plate_file_path)
    picture_plate(plate_image)

    # plate_video = cv.VideoCapture(plate_file_path)
    # images = vs.get_video_seperated(plate_video)
    # video_plate(images)
