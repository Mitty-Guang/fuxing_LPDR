from models.ocr_net2 import OcrNet
from models import ocr_config as config
import torch
import cv2
import os


class Explorer:

    def __init__(self, is_cuda=False):
        self.device = config.device
        self.net = OcrNet(config.num_class)
        if os.path.exists(config.weight):
            self.net.load_state_dict(torch.load(config.weight, map_location='cpu'))
        else:
            raise RuntimeError('Model parameters are not loaded')
        self.net = self.net.to(self.device).eval()

    def __call__(self, image):
        with torch.no_grad():
            # cv2.imwrite('a.jpg',image)
            image = torch.from_numpy(image).permute(2, 0, 1) / 255
            image = image.unsqueeze(0).to(self.device)
            # print(self.net.state_dict())
            out = self.net(image).reshape(-1, 70)
            # print(out.shape)
            out = torch.argmax(out, dim=1)
            # print(out)
            out = out.cpu().numpy().tolist()
            c = ''
            for i in out:
                c += config.class_name[i]
            return self.deduplication(c)

    def deduplication(self, c):
        '''符号去重'''
        temp = ''
        new = ''
        for i in c:
            if i == temp:
                continue
            else:
                if i == '*':
                    temp = i
                    continue
                new += i
                temp = i
        return new
