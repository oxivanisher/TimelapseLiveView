#!/usr/bin/env python3

import time
from os import walk, path, getenv, stat, unlink
from flask import Flask, render_template, request, abort, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './static'
ALLOWED_EXTENSIONS = ['.png', '.jpg', '.jpeg', '.gif']

app = Flask(__name__)
# config
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


# Helper functions
def allowed_file(file_path):
    app.logger.debug('checking if file %s has allowed extension', file_path)
    file_name, file_extension = path.splitext(file_path)
    if file_extension in ALLOWED_EXTENSIONS:
        app.logger.debug('%s has allowed extension', file_path)
        return True
    return False


def check_file_age(file_name):
    if stat(path.join(UPLOAD_FOLDER, file_name)).st_mtime < time.time() - 15 * 60:
        unlink(path.join(UPLOAD_FOLDER, file_name))
        app.logger.warning("Removed file %s due to age older than 15 minutes" % file_name)
        return False
    return True


@app.route('/')
def index():
    cameras = []
    for (dir_path, dir_names, file_names) in walk(UPLOAD_FOLDER):
        for file_name in file_names:
            if allowed_file(file_name):
                if check_file_age(file_name):
                    cameras.append(file_name)
    app.logger.debug('cameras found: %s', cameras)
    return render_template('index.html.jinja2', cameras=cameras)


@app.route('/viewer/<camera>')
def viewer(camera):
    if check_file_age(camera):
        return render_template('viewer.html.jinja2', camera=camera)
    return redirect(url_for('index'))


@app.route('/upload/<requested_file_name>', methods=['POST', 'PUT'])
def upload(requested_file_name):
    if request.form.get("upload_key") != getenv('UPLOAD_KEY'):
        app.logger.warning('upload key wrong <%s>. It should be <%s>' % (request.form.get("upload_key"),
                                                                         getenv('UPLOAD_KEY')))
        abort(401)

    file = request.files['file']
    requested_file_name = secure_filename(requested_file_name)
    file.save(path.join(app.config['UPLOAD_FOLDER'], requested_file_name))
    return requested_file_name


if __name__ == "__main__":
    app.run(host='0.0.0.0')
