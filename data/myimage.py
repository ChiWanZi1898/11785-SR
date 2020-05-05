import os
import os.path
import random
import math
import errno

from data import common

import numpy as np
import scipy.misc as misc
import imageio

import torch
import torch.utils.data as data
from torchvision import transforms

class MyImage(data.Dataset):
    def __init__(self, args, train=False):
        self.args = args
        self.train = False
        self.name = 'MyImage'
        self.scale = args.scale
        self.idx_scale = 0
        # apath = args.testpath + '/' + args.testset + '/x' + str(args.scale[0])
        apath = args.testpath

        self.filelist = []
        self.imnamelist = []
        if not train:
            for f in os.listdir(apath):
                try:
                    filename = os.path.join(apath, f)
                    # imageio.imread(filename)
                    self.filelist.append(filename)
                    self.imnamelist.append(f)
                except Exception as e:
                    print(e)
        self.filelist = sorted(self.filelist)
        split_len = (len(self.filelist) - 1) // args.split_num + 1
        self.filelist = self.filelist[
                        args.split_idx * split_len:min((args.split_idx + 1) * split_len, len(self.filelist))]

    def __getitem__(self, idx):
        filename = os.path.split(self.filelist[idx])[-1]
        filename, _ = os.path.splitext(filename)
        lr = imageio.imread(self.filelist[idx])
        lr = common.set_channel([lr], self.args.n_colors)[0]

        return common.np2Tensor([lr], self.args.rgb_range)[0], -1, filename, 0

    def __len__(self):
        return len(self.filelist)

    def set_scale(self, idx_scale):
        self.idx_scale = idx_scale
