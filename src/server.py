import os
from io import BytesIO
from PIL import Image
from flask import Flask, jsonify, request, send_file, session
from werkzeug.utils import secure_filename
from cv2 import imwrite

import processbreadboard as cvprocess

UPLOAD_FOLDER = 'images'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/image', methods=['POST'])
def upload_file():
    """Handles the upload of an image."""
    d = {}
    try:
        file = request.files['image']
        file_bytes = file.read()
        img = Image.open(BytesIO(file_bytes))

        #save image
        if img:
            filename = secure_filename(file.filename)
            img_loc = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            img.save(img_loc)
        
            #image processing
            chips, endpoints, cropped_img, chip_bounding = cvprocess.process_image(img_loc)
            imwrite(img_loc, cropped_img)
            session['img_loc'] = img_loc
            session['chips'] = chip_bounding

        d['status'] = 1

    except Exception as e:
        print(f"Couldn't upload file {e}")
        d['status'] = 0

    return jsonify(d)

@app.route('/chipinfo', methods=['POST'])
def update_chips():
    d= {}
    try:
        print(request.form['chips'])
        d['status'] = 1

    except Exception as e:
        print(f"Couldn't update chip data")
        d['status'] = 0
    return jsonify(d)

@app.route('/chips', methods=['GET'])
def get_chips():
    if 'chips' in session:
        return jsonify(session['chips'])
    return 0

@app.route('/croppedimage', methods=['GET'])
def get_cropped_image():
    if 'img_loc' in session:
        return send_file(session['img_loc'])
    return 0

if __name__ == "__main__":
    app.secret_key = "My Secret key"
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True, port=8000)
