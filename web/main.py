from flask import Flask, request, render_template, send_from_directory
import os
import sys
import time
import base64

app = Flask(__name__, template_folder='www')

in_images_dir = 'in_images'
out_images_dir = 'out_images'


@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    req_time = time.time()
    file_id = str(base64.urlsafe_b64encode(bytes(str(req_time),encoding='utf8')))
    file.save(os.path.join(in_images_dir, file_id))
    file_id = 'lyl.jpg'
    # todo: process image and get id.
    return render_template('view.html', in_image_name=file_id, out_image_name=file_id)


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
    if not os.path.isdir(in_images_dir):
        os.mkdir(in_images_dir)
    if not os.path.isdir(out_images_dir):
        os.mkdir(out_images_dir)


if __name__ == '__main__':
    setup()
    listen_port = 8080
    if len(sys.argv) > 1:
        listen_port = int(sys.argv[1])

    app.run(port=listen_port, debug=True)
