import utility
import model
from option import args

import numpy as np
import torch
import imageio

torch.manual_seed(args.seed)
checkpoint = utility.checkpoint(args)


def process(model, in_path, out_path):
    lr = imageio.imread(in_path)
    lr = torch.FloatTensor(lr).cuda()
    lr = lr.permute(2, 0, 1).unsqueeze(0)
    model.eval()
    with torch.no_grad():
        sr = model(lr, 0)
    sr = sr.permute(0, 2, 3, 1)
    sr = sr.clamp(0, 255).round()
    sr = sr[0].detach().cpu().numpy().astype(np.uint8)

    imageio.imsave(out_path, sr)


if checkpoint.ok:
    model = model.Model(args, checkpoint)

    process(model, './images/in.png', './images/out.png')
