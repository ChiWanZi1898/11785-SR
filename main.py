import utility
from option import args
import model as _model

import numpy as np
import torch
import imageio

from flask import Flask, request, render_template, send_from_directory
import os
import time
import base64

app = Flask(__name__, template_folder='www')

in_images_dir = 'in_images'
out_images_dir = 'out_images'
global_model = None


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


@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    req_time = time.time()
    file_id = str(req_time) + '.png'
    print('File id is:', file_id)
    full_in_path = os.path.join(in_images_dir, file_id)
    full_out_path = os.path.join(out_images_dir, file_id)
    file.save(full_in_path)
    process(global_model, full_in_path, full_out_path)
    # todo: process image and get id.
    return render_template('view.html', in_image_name=file_id, out_image_name=file_id)

@app.route('/uploadImage', methods=['POST'])
def upload_file_api():
    file = request.files['file']
    req_time = time.time()
    file_id = str(req_time) + '.png'
    print('File id is:', file_id)
    full_in_path = os.path.join(in_images_dir, file_id)
    full_out_path = os.path.join(out_images_dir, file_id)
    file.save(full_in_path)
    process(global_model, full_in_path, full_out_path)
    # todo: process image and get id.
    return send_from_directory('out_images', file_id)


@app.route('/view', methods=['GET'])
def view_images():
    file_id = request.args.get('id')
    return render_template('view.html', in_image_name=file_id, out_image_name=file_id)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/out_images/<path:path>')
def static_out(path):
    return send_from_directory('out_images', path)


@app.route('/in_images/<path:path>')
def static_in(path):
    return send_from_directory('in_images', path)


def setup():
    torch.manual_seed(args.seed)
    checkpoint = utility.checkpoint(args)
    if checkpoint.ok:
        s1 = time.time()
        model = _model.Model(args, checkpoint)
        s2 = time.time()
        print('load model time:', s2 - s1)
    else:
        print("load model error")
        exit(-1)

    if not os.path.isdir(in_images_dir):
        os.mkdir(in_images_dir)
    if not os.path.isdir(out_images_dir):
        os.mkdir(out_images_dir)

    return model


if __name__ == '__main__':
    global_model = setup()
    listen_port = 8080
    if args.listen_port:
        listen_port = args.listen_port

    print("start server listen at:", listen_port)
    app.run(port=listen_port, debug=True, host='0.0.0.0')
