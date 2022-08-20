# 视频的分割，每 m 帧切分为一张图片
# 参数：视频 video
# 返回值：图片集 images
def get_video_seperated(video):
    images = []
    # 读帧
    success, frame = video.read()
    # 每 50 帧读取一张图片
    timeF = 50
    i = 0
    while success:
        i = i + 1
        if i % timeF == 0:
            images.append(frame)
        success, frame = video.read()
    return images



