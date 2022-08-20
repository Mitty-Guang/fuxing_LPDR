import os
import os.path
import re
import shutil
import random

import cv2
from tqdm import tqdm


def listPathAllfiles(dirname):
    result = []
    for maindir, subdir, file_name_list in os.walk(dirname):
        for filename in file_name_list:
            apath = os.path.join(maindir, filename)
            result.append(apath)
    return result


if __name__ == '__main__':
    data_path = r'C:\study\WorkSpace\dataset\CCPD2019'
    save_path = r'C:\study\WorkSpace\dataset\CCPD_for_me'  # 程序会存到这个路径 C:\study\WorkSpace\dataset\CCPD2019
    images_files = listPathAllfiles(data_path)
    random.shuffle(images_files)

    cnt = 1
    for name in tqdm(images_files):
        if (name.endswith(".jpg") or name.endswith(".png")) and cnt < 1000:  # 100000
            if cnt < 600:
                images_save_path = os.path.join(save_path, "train\images")
                labels_save_path = os.path.join(save_path, "train\labels")
            elif 600 <= cnt < 800:
                images_save_path = os.path.join(save_path, "test\images")
                labels_save_path = os.path.join(save_path, "test\labels")
            else:
                images_save_path = os.path.join(save_path, "val\images")
                labels_save_path = os.path.join(save_path, "val\labels")
            if not os.path.exists(images_save_path):
                os.makedirs(images_save_path)
            if not os.path.exists(labels_save_path):
                os.makedirs(labels_save_path)
            img = cv2.imread(name)
            height, width = img.shape[0], img.shape[1]

            # 提取四个角
            str1 = re.findall('-\d+\&\d+_\d+\&\d+-', name)[0][1:-1]
            str2 = re.split('\&|_', str1)
            x0 = int(str2[0])
            y0 = int(str2[1])
            x1 = int(str2[2])
            y1 = int(str2[3])

            x = round((x0 + x1) / 2 / width, 6)  # 四舍五入
            y = round((y0 + y1) / 2 / height, 6)
            w = round((x1 - x0) / width, 6)
            h = round((y1 - y0) / height, 6)

            txtfile = os.path.join(labels_save_path, "plate_" + str(cnt).zfill(6) + ".txt")
            imgfile = os.path.join(images_save_path,
                                   "plate_" + str(cnt).zfill(6) + "." + os.path.basename(name).split(".")[-1])

            open(txtfile, "w").write(" ".join(["0", str(x), str(y), str(w), str(h)]))
            shutil.copy(name, imgfile)  # 复制文件到别的位置，且重命名

            cnt += 1
