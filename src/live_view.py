#!/usr/bin/env python3

from os import walk, path, getenv
from flask import Flask, render_template, request, abort
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './static'
ALLOWED_EXTENSIONS = ['.png', '.jpg', '.jpeg', '.gif']

app = Flask(__name__)
# config
app.config["DEBUG"] = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Helper functions
def allowed_file(file_path):
    app.logger.debug('checking if file %s has allowed extension', file_path)
    file_name, file_extension = path.splitext(file_path)
    if file_extension in ALLOWED_EXTENSIONS:
        app.logger.debug('%s has allowed extension', file_path)
        return True
    return False


@app.route('/')
def index():
    cameras = []
    for (dir_path, dir_names, file_names) in walk(UPLOAD_FOLDER):
        for file_name in file_names:
            if allowed_file(file_name):
                cameras.append(file_name)
    app.logger.debug('cameras found: %s', cameras)
    return render_template('index.html.jinja2', cameras=cameras)


@app.route('/viewer/<camera>')
def viewer(camera):
    return render_template('viewer.html.jinja2', camera=camera)


@app.route('/upload/<requested_file_name>', methods=['POST', 'PUT'])
def upload(requested_file_name):
    if request.form.get("upload_key") != getenv('UPLOAD_KEY'):
        app.logger.error('upload key wrong: %s', request.form.get("upload_key"))
        abort(401)

    file = request.files['file']
    requested_file_name = secure_filename(requested_file_name)
    file.save(path.join(app.config['UPLOAD_FOLDER'], requested_file_name))
    return requested_file_name


if __name__ == "__main__":
    app.run(host='0.0.0.0')
