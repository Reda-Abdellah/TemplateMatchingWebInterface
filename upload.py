
from flask import Flask, render_template, request,redirect
from flask_uploads import UploadSet, configure_uploads, IMAGES
import os
import tm
from flask import send_file
import before_download

app = Flask(__name__, static_url_path = "", static_folder = "static")

photos = UploadSet('photos', IMAGES)

app.config['UPLOADED_PHOTOS_DEST'] = 'static/img'
app.config['UPLOADED_TEMPLATES_DEST'] = 'static/temp'

configure_uploads(app, photos)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST' and 'photos' in request.files:
        for f in request.files.getlist('photos'):
            f.save(os.path.join(app.config['UPLOADED_PHOTOS_DEST'], f.filename))
        for f in request.files.getlist('templates'):
            f.save(os.path.join(app.config['UPLOADED_TEMPLATES_DEST'], f.filename))

        tm.main()
        before_download.main()

        return render_template('downloads.html')

    return render_template('upload.html')
    #


@app.route('/file-downloads/')
def file_downloads():
    try:
        return render_template('downloads.html')

    except Exception as e:
        return str(e)


@app.route('/return-files/')
def return_files_tut():
    return send_file('static/result.zip', attachment_filename='result.zip')
    """
    try:
        return send_file('static/result.zip', attachment_filename='result.zip')
    except Exception as e:
		return str(e)
    """

if __name__ == '__main__':
    app.run(debug=True)
