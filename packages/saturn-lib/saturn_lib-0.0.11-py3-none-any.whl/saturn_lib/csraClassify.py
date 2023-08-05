# -*- coding: utf-8  -*-
# -*- author: jokker -*-

import os
import cv2
import torch
import configparser
import numpy as np
import uuid
from .abstractBase import detection
#
import torch.nn as nn
from PIL import Image
from torch.utils.data import DataLoader
from torchvision.transforms import transforms
from .csra_libs.pipeline.resnet_csra import ResNet_CSRA
from .csra_libs.pipeline.vit_csra import VIT_B16_224_CSRA, VIT_L16_224_CSRA, VIT_CSRA
from .csra_libs.pipeline.dataset import DataSet
from .csra_libs.utils.evaluation.eval import voc_classes, wider_classes, coco_classes, class_dict


class CsraClassify(detection):

    def __init__(self, section, cfg_path, gpu_id, model_path=None):
        super(CsraClassify, self).__init__(section=section, cfg_path=cfg_path)
        self.section = section
        self.gpu_id = gpu_id
        self.model_path = model_path
        self.classes = tuple(self.classes.strip(',').split(','))
        self.device = self.select_device(self.gpu_id)
        #
        normalize = transforms.Normalize(mean=[0, 0, 0], std=[1, 1, 1])
        self.transform = transforms.Compose([
            transforms.Resize((int(self.img_size), int(self.img_size))),
            transforms.ToTensor(),
            normalize])

    def model_restore(self):
        """加载模型"""
        try:
            if not self.model_path:
                raise ValueError("model path is None")

            self.model = ResNet_CSRA(num_heads=1, lam=0.1, num_classes=4)
            self.model.load_state_dict(torch.load(self.model_path))
            #
            self.model.to(self.device)
            self.model.eval()
            self.warmUp()
            print("* load csraClassify model success : {0}".format(self.section))
        except Exception as e:
            print(e)
            raise ValueError("* load csraClassify model failed : {0}".format(self.section))

    def warmUp(self):
        im = 123 * np.ones((224, 224, 3), dtype=np.uint8)
        self.detect(im)

    @torch.no_grad()
    def detect(self, im, image_name='test.jpg'):
        """进行检测"""

        im = Image.fromarray(im)
        img = self.transform(im)
        img = img.cuda()
        img = img.unsqueeze(0)
        #
        logit = self.model(img)
        logit = logit.squeeze(0)
        logit = nn.Sigmoid()(logit)
        pos = torch.where(logit > 0.5)[0].cpu().numpy()
        #
        res_list = []
        for k in pos:
            res_list.append(self.classes[k])
        return res_list













