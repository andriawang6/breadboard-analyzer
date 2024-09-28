import os
from io import BytesIO
from PIL import Image
from flask import Flask, jsonify, request
from werkzeug.utils import secure_filename
import base64

UPLOAD_FOLDER = 'images'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/image', methods=['POST'])
def upload_file():
    """Handles the upload of a file."""
    d = {}
    try:
        file = request.files['image']
        #print(f"Uploading file {filename}")
        file_bytes = file.read()
        img = Image.open(BytesIO(file_bytes))

        #save image
        if img:
            filename = secure_filename(file.filename)
            img.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        d['status'] = 1

    except Exception as e:
        print(f"Couldn't upload file {e}")
        d['status'] = 0

    return jsonify(d)


if __name__ == "__main__":
    app.run(debug=True)
