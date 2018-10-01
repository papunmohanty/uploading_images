__author__ = 'Papun Mohanty'

import os
from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory, Request
from werkzeug.utils import secure_filename
from werkzeug import SharedDataMiddleware


UPLOAD_FOLDER = "static/images/"
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
BASE_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)
app.config['SECRET_KEY'] = 'asecretkey'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        print("The file is: ", type(file))
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        print("Th file name is: ", file.filename)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # return redirect(url_for('uploaded_file', filename=filename))
    return render_template('uploadform.html')


@app.route('/uploaded_file')
def uploaded_file():
    list_images = os.listdir(UPLOAD_FOLDER)
    return render_template('uploaded_file.html', files=list_images, folder=UPLOAD_FOLDER)



# @app.route('/uploads/<filename>')
# def uploaded_file(filename):
#     return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


# app.add_url_rule('/uploads/<filename>', 'uploaded_file', build_only=True)
# app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
#     '/uploads':  app.config['UPLOAD_FOLDER']
# })


if __name__ == '__main__':
    app.run(debug=True)

