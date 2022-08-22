# YOLOv5 🚀 by Ultralytics, GPL-3.0 license
"""
Run inference on images, videos, directories, streams, etc.

Usage - sources:
    $ python path/to/detect.py --weights yolov5s.pt --source 0              # webcam
                                                             img.jpg        # image
                                                             vid.mp4        # video
                                                             path/          # directory
                                                             path/*.jpg     # glob
                                                             'https://youtu.be/Zgi9g1ksQHc'  # YouTube
                                                             'rtsp://example.com/media.mp4'  # RTSP, RTMP, HTTP stream

Usage - formats:
    $ python path/to/detect.py --weights yolov5s.pt                 # PyTorch
                                         yolov5s.torchscript        # TorchScript
                                         yolov5s.onnx               # ONNX Runtime or OpenCV DNN with --dnn
                                         yolov5s.xml                # OpenVINO
                                         yolov5s.engine             # TensorRT
                                         yolov5s.mlmodel            # CoreML (MacOS-only)
                                         yolov5s_saved_model        # TensorFlow SavedModel
                                         yolov5s.pb                 # TensorFlow GraphDef
                                         yolov5s.tflite             # TensorFlow Lite
                                         yolov5s_edgetpu.tflite     # TensorFlow Edge TPU
"""

import argparse
import os
import sys
from pathlib import Path

import cv2
import torch
import torch.backends.cudnn as cudnn

FILE = Path(__file__).resolve()  # __file__指的是当前文件(即detect.py),FILE最终保存着当前文件的绝对路径
ROOT = FILE.parents[0]  # ROOT保存着当前项目的父目录
if str(ROOT) not in sys.path: # sys.path即当前python环境可以运行的路径,假如当前项目不在该路径中,就无法运行其中的模块,所以就需要加载路径
    sys.path.append(str(ROOT))  # 把ROOT添加到运行路径上
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # ROOT设置为相对路径

from models.common import DetectMultiBackend
from utils.datasets import IMG_FORMATS, VID_FORMATS, LoadImages, LoadStreams
from utils.general import (LOGGER, check_file, check_img_size, check_imshow, check_requirements, colorstr,
                           increment_path, non_max_suppression, print_args, scale_coords, strip_optimizer, xyxy2xywh)
from utils.plots import Annotator, colors, save_one_box
from utils.torch_utils import select_device, time_sync


@torch.no_grad()  # 该标注使得方法中所有计算得出的tensor的requires_grad都自动设置为False，也就是说不会求梯度，可以加快预测效率，减小资源消耗
def run(weights=ROOT / 'best.pt',  # 事先训练完成的权重文件
        source=ROOT / 'data/images',  # 预测时的输入数据，可以是文件/路径/URL/glob, 输入是0的话调用摄像头作为输入
        data=ROOT / 'data/ccpd.yaml',  # 数据集文件
        imgsz=(640, 640),  # 预测时的放缩后图片大小 (height, width)
        conf_thres=0.25,  # 置信度阈值
        iou_thres=0.45,  # IOU阈值
        max_det=1000,  # 一张图片上检测的最大目标数量
        device='',  # 所使用的GPU编号
        view_img=False,  # 是否在推理时预览图片
        save_txt=False,  # 是否将结果保存在txt文件中
        save_conf=False,  # 是否将结果中的置信度保存在txt文件中
        save_crop=False,  # 是否保存裁剪后的预测框
        nosave=False,  # 是否保存预测后的图片/视频
        classes=None,  # 过滤指定类的预测结果
        agnostic_nms=False,  # 如为True,则为class-agnostic. 否则为class-specific
        augment=False,  # augmented inference
        visualize=False,  # visualize features
        update=False,  # update all models
        project=ROOT / 'runs/detect',  # 推理结果保存的路径
        name='exp',  # 结果保存文件夹的命名前缀
        exist_ok=False,  # True: 推理结果覆盖之前的结果 False: 推理结果新建文件夹保存,文件夹名递增
        line_thickness=3,  # 绘制Bounding_box的线宽度
        hide_labels=False,  # True: 隐藏标签
        hide_conf=False,  # True: 隐藏置信度
        half=False,  # use FP16 half-precision inference 是否使用半精度推理（节约显存）
        dnn=False,  # use OpenCV DNN for ONNX inference
        ):
    source = str(source)
    save_img = not nosave and not source.endswith('.txt')  # 是否需要保存图片,如果nosave为false且source的结尾不是txt则保存图片
    is_file = Path(source).suffix[1:] in (IMG_FORMATS + VID_FORMATS)  # 判断source是不是视频/图像文件路径
    is_url = source.lower().startswith(('rtsp://', 'rtmp://', 'http://', 'https://'))  # 判断source是否是链接
    webcam = source.isnumeric() or source.endswith('.txt') or (is_url and not is_file)  # 判断是source是否是摄像头
    if is_url and is_file:
        source = check_file(source)  # download

    # Directories
    save_dir = increment_path(Path(project) / name, exist_ok=exist_ok)  # increment run
    (save_dir / 'labels' if save_txt else save_dir).mkdir(parents=True, exist_ok=True)  # make dir

    # Load model
    device = select_device(device)
    model = DetectMultiBackend(weights, device=device, dnn=dnn, data=data)
    stride, names, pt, jit, onnx, engine = model.stride, model.names, model.pt, model.jit, model.onnx, model.engine
    # stride：推理时所用到的步长，默认为32， 大步长适合于大目标，小步长适合于小目标
    # names：保存推理结果名的列表，比如默认模型的值是['person', 'bicycle', 'car', ...]
    # pt: 加载的是否是pytorch模型（也就是pt格式的文件）
    imgsz = check_img_size(imgsz, s=stride)  # check image size

    # Half
    half &= (pt or jit or onnx or engine) and device.type != 'cpu'  # FP16 supported on limited backends with CUDA
    if pt or jit:
        model.model.half() if half else model.model.float()

    # Dataloader
    if webcam:  # 使用摄像头作为输入
        view_img = check_imshow()
        cudnn.benchmark = True  # set True to speed up constant image size inference
        dataset = LoadStreams(source, img_size=imgsz, stride=stride, auto=pt)
        bs = len(dataset)  # batch_size
    else:
        dataset = LoadImages(source, img_size=imgsz, stride=stride, auto=pt)
        bs = 1  # batch_size
    vid_path, vid_writer = [None] * bs, [None] * bs

    # Run inference
    model.warmup(imgsz=(1 if pt else bs, 3, *imgsz), half=half)  # 热身
    dt, seen = [0.0, 0.0, 0.0], 0
    # seen: 已经处理完了多少帧图片
    # dt: 存储每一步骤的耗时
    for path, im, im0s, vid_cap, s in dataset:
        # 在dataset中，每次迭代的返回值是self.sources, img, img0, None, ''
        # path: 文件路径（即source）
        # im: 处理后的输入图片列表（经过了放缩操作）
        # im0s: 源输入图片列表
        # vid_cap
        # s: 图片的基本信息，比如路径，大小
        t1 = time_sync()  # 获取当前时间
        im = torch.from_numpy(im).to(device)
        im = im.half() if half else im.float()  # uint8 to fp16/32
        im /= 255  # 0 - 255 to 0.0 - 1.0 --归一化
        if len(im.shape) == 3:
            im = im[None]  # expand for batch dim
        t2 = time_sync()
        dt[0] += t2 - t1

        # Inference
        visualize = increment_path(save_dir / Path(path).stem, mkdir=True) if visualize else False
        # 如果为True则保留推理过程中的特征图，保存在runs文件夹中
        pred = model(im, augment=augment, visualize=visualize)
        # 推理结果，pred保存的是所有的bound_box的信息
        t3 = time_sync()
        dt[1] += t3 - t2

        # NMS
        pred = non_max_suppression(pred, conf_thres, iou_thres, classes, agnostic_nms, max_det=max_det)
        # 执行非极大值抑制，返回值为过滤后的预测框
        # conf_thres: 置信度阈值
        # iou_thres: iou阈值
        # classes: 需要过滤的类（数字列表）
        # agnostic_nms： 标记class-agnostic或者使用class-specific方式。默认为class-agnostic
        # max_det: 检测框结果的最大数量
        dt[2] += time_sync() - t3

        # Second-stage classifier (optional)
        # pred = utils.general.apply_classifier(pred, classifier_model, im, im0s)

        # Process predictions
        for i, det in enumerate(pred):  # per image
            seen += 1
            if webcam:  # batch_size >= 1
                p, im0, frame = path[i], im0s[i].copy(), dataset.count
                s += f'{i}: '
            else:
                p, im0, frame = path, im0s.copy(), getattr(dataset, 'frame', 0)

            p = Path(p)  # to Path
            save_path = str(save_dir / p.name)  # 推理结果图片保存的路径
            txt_path = str(save_dir / 'labels' / p.stem) + ('' if dataset.mode == 'image' else f'_{frame}')  # im.txt
            s += '%gx%g ' % im.shape[2:]  # 显示推理前裁剪后的图像尺寸
            gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  # normalization gain whwh
            imc = im0.copy() if save_crop else im0  # for save_crop
            # 如果save_crop的值为true， 则将检测到的bounding_box单独保存成一张图片。
            annotator = Annotator(im0, line_width=line_thickness, example=str(names))
            # 得到一个绘图的类，类中预先存储了原图、线条宽度、类名
            if len(det):
                # Rescale boxes from img_size to im0 size
                det[:, :4] = scale_coords(im.shape[2:], det[:, :4], im0.shape).round()
                # 将标注的bounding_box大小调整为和原图一致（因为训练时原图经过了放缩）

                # Print results
                for c in det[:, -1].unique():
                    n = (det[:, -1] == c).sum()  # detections per class
                    s += f"{n} {names[int(c)]}{'s' * (n > 1)}, "  # add to string
                # 打印出所有的预测结果  比如1 person（检测出一个人）

                # Write results
                for *xyxy, conf, cls in reversed(det):
                    if save_txt:  # Write to file
                        xywh = (xyxy2xywh(torch.tensor(xyxy).view(1, 4)) / gn).view(-1).tolist()  # normalized xywh
                        line = (cls, *xywh, conf) if save_conf else (cls, *xywh)  # label format
                        with open(txt_path + '.txt', 'a') as f:
                            f.write(('%g ' * len(line)).rstrip() % line + '\n')
                        # 写入对应的文件夹里，路径默认为“runs\detect\exp*\labels”

                    if save_img or save_crop or view_img:  # Add bbox to image
                        c = int(cls)  # integer class
                        label = None if hide_labels else (names[c] if hide_conf else f'{names[c]} {conf:.2f}')
                        annotator.box_label(xyxy, label, color=colors(c, True))
                        if save_crop:  # 将预测框内的图片单独保存
                            if os.path.isdir(save_dir / 'crops/plate'):
                                file_lis = os.listdir(save_dir / 'crops/plate')
                                for file_name in file_lis:
                                    tf = os.path.join(save_dir / 'crops/plate', file_name)
                                    if not os.path.isdir(tf):
                                        os.remove(tf)
                            save_one_box(xyxy, imc, file=save_dir / 'crops' / names[c] / f'{p.stem}.jpg', BGR=True)

            # Stream results
            im0 = annotator.result()  # im0是绘制好的图片

            if view_img:  # 如果view_img为true,则显示该图片
                cv2.imshow(str(p), im0)
                cv2.waitKey(1)  # 1 millisecond

            # Save results (image with detections)
            if save_img:  # 如果save_img为true,则保存绘制完的图片
                if dataset.mode == 'image':
                    cv2.imwrite(save_path, im0)
                else:  # 'video' or 'stream'
                    if vid_path[i] != save_path:  # new video
                        vid_path[i] = save_path
                        if isinstance(vid_writer[i], cv2.VideoWriter):
                            vid_writer[i].release()  # release previous video writer
                        if vid_cap:  # video
                            fps = vid_cap.get(cv2.CAP_PROP_FPS)
                            w = int(vid_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                            h = int(vid_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                        else:  # stream
                            fps, w, h = 30, im0.shape[1], im0.shape[0]
                        save_path = str(Path(save_path).with_suffix('.mp4'))  # force *.mp4 suffix on results videos
                        vid_writer[i] = cv2.VideoWriter(save_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (w, h))
                    vid_writer[i].write(im0)

        # Print time (inference-only)
        LOGGER.info(f'{s}Done. ({t3 - t2:.3f}s)')

    # Print results
    t = tuple(x / seen * 1E3 for x in dt)  # 平均每张图片所耗费时间
    LOGGER.info(f'Speed: %.1fms pre-process, %.1fms inference, %.1fms NMS per image at shape {(1, 3, *imgsz)}' % t)
    if save_txt or save_img:
        s = f"\n{len(list(save_dir.glob('labels/*.txt')))} labels saved to {save_dir / 'labels'}" if save_txt else ''
        LOGGER.info(f"Results saved to {colorstr('bold', save_dir)}{s}")
    if update:
        strip_optimizer(weights)  # update model (to fix SourceChangeWarning)


def parse_opt(image_path):
    parser = argparse.ArgumentParser()

    '''
    weight: 训练的权重
    source: 测试数据，图片/视频路径/‘0’（电脑自带摄像头）等
    img-size: 网络输入图片大小
    conf-thres: 置信度阈值
    iou-thres: 做nms的iou阈值
    device: 设置设备
    view-img: 是否展示预测之后的图片/视频，默认False
    save-txt: 是否将预测的框坐标以txt文件形式保存，默认False
    save-dir: 网络预测之后的图片/视频的保存路径
    classes: 设置只保留某一部分类别
    agnostic-nms: 进行nms是否也去除不同类别之间的框，默认False
    augment: 推理的时候进行多尺度，翻转等操作（TTA）推理
    update: 如果为True，则对所有模型进行strip_optimizer操作，去除pt文件中优化器等信息，默认为False
    '''
    parser.add_argument('--weights', nargs='+', type=str, default=ROOT / 'model_train/best.pt', help='model path(s)')
    parser.add_argument('--source', type=str, default=image_path, help='file/dir/URL/glob, 0 for webcam')
    parser.add_argument('--data', type=str, default=ROOT / 'data/ccpd.yaml', help='(optional) dataset.yaml path')
    parser.add_argument('--imgsz', '--img', '--img-size', nargs='+', type=int, default=[640], help='inference size h,w')
    parser.add_argument('--conf-thres', type=float, default=0.25, help='confidence threshold')
    parser.add_argument('--iou-thres', type=float, default=0.45, help='NMS IoU threshold')
    parser.add_argument('--max-det', type=int, default=1000, help='maximum detections per image')
    parser.add_argument('--device', default='', help='cuda device, i.e. 0 or 0,1,2,3 or cpu')
    parser.add_argument('--view-img', action='store_true', help='show results')
    parser.add_argument('--save-txt', action='store_true', help='save results to *.txt')
    parser.add_argument('--save-conf', action='store_true', help='save confidences in --save-txt labels')
    parser.add_argument('--save-crop', action='store_true', default=True, help='save cropped prediction boxes')
    parser.add_argument('--nosave', action='store_true', help='do not save images/videos')
    parser.add_argument('--classes', nargs='+', type=int, help='filter by class: --classes 0, or --classes 0 2 3')
    parser.add_argument('--agnostic-nms', action='store_true', help='class-agnostic NMS')
    parser.add_argument('--augment', action='store_true', help='augmented inference')
    parser.add_argument('--visualize', action='store_true', help='visualize features')
    parser.add_argument('--update', action='store_true', help='update all models')
    parser.add_argument('--project', default=ROOT / 'runs/detect', help='save results to project/name')
    parser.add_argument('--name', default='exp', help='save results to project/name')
    parser.add_argument('--exist-ok', action='store_true', default=True, help='existing project/name ok, do not increment')
    parser.add_argument('--line-thickness', default=3, type=int, help='bounding box thickness (pixels)')
    parser.add_argument('--hide-labels', default=False, action='store_true', help='hide labels')
    parser.add_argument('--hide-conf', default=False, action='store_true', help='hide confidences')
    parser.add_argument('--half', action='store_true', help='use FP16 half-precision inference')
    parser.add_argument('--dnn', action='store_true', help='use OpenCV DNN for ONNX inference')
    opt = parser.parse_args()
    opt.imgsz *= 2 if len(opt.imgsz) == 1 else 1  # expand
    print_args(FILE.stem, opt)
    return opt


def main(opt):
    check_requirements(exclude=('tensorboard', 'thop'))
    run(**vars(opt))

