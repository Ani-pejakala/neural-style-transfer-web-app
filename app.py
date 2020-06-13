from flask import Flask, render_template, request, send_file
import os
from run_model import forward_pass

app = Flask(__name__)
UPLOAD_FOLDER = "/static/uploads/images/"
STYLE_PATH = 'static/uploads/style_images/'


@app.route('/', methods=['GET', 'POST'])
def home_page():
    if request.method == 'POST':
        # check if the post request has the file part
        style = request.form.get('style')
        if 'file' not in request.files:
            return render_template('index.html', msg='No file selected')
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            return render_template('index.html', msg='No file selected')

        if file and style:
            print(os.path.join(UPLOAD_FOLDER, file.filename))
            #files_to_delete = [os.path.join(UPLOAD_FOLDER, f) for f in os.listdir(UPLOAD_FOLDER)]
            #for f in files_to_delete:
               #sos.remove(f)
            file.save(os.path.join(os.getcwd() + UPLOAD_FOLDER, file.filename))
            out = forward_pass(style, file.filename, style)
            # print(out)
            filename, file_extension = os.path.splitext(file.filename)
            return render_template('result.html', image=UPLOAD_FOLDER + file.filename,
                                   style_image=STYLE_PATH + filename +'_'+ style.split('.')[0] + file_extension, style=style)
        else:
            return render_template('index.html', msg='No style selected')

    elif request.method == 'GET':
        return render_template('index.html')


@app.route('/download/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    print(filename)
    return send_file(filename, as_attachment=True)


# @app.route('/upload', methods=['GET', 'POST'])
# def upload_page():

if __name__ == '__main__':
    app.run()
