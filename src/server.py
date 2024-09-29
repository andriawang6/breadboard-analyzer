import os
from io import BytesIO
from PIL import Image
from flask import Flask, jsonify, request, send_file, session
from werkzeug.utils import secure_filename
from cv2 import imwrite
import json

import processbreadboard as cvprocess

import datasheets
import logicanalysis.logic_processing
import logicanalysis.generate_logic
import logicanalysis.draw_schematic
from schemdraw.parsing import logicparse


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
            session['chip_coords'] = chips
            session['endpoints'] = endpoints
            
            # reprocess session['endpoints'] to delete garbage data
            prev = ()
            res = []
            for endpoint in session['endpoints']:
                if endpoint[0] == endpoint[1]:
                    continue
                if endpoint == prev:
                    continue
                prev = endpoint
                res.append(endpoint)
            session['endpoints'] = res


        d['status'] = 1

    except Exception as e:
        print(f"Couldn't upload file {e}")
        d['status'] = 0

    return jsonify(d)

@app.route('/chipinfo', methods=['POST'])
def update_chips():
    d= {}
    try:
        chip_types = request.form['chips'] #array of chip types in the correct order 
        chip_types = chip_types.split(",")

        if not 'chip_coords' in session: return 0

        #iterate through chip coords and update type
        count = 0
        for chip in session["chip_coords"]:
            session["chip_coords"][chip][0] = chip_types[count]
            count += 1
        print(f"chip coords now processed: {session['chip_coords']}")
        session['updated_chip_coords'] = session['chip_coords']
        d['status'] = 1

    except Exception as e:
        print(f"Couldn't update chip data {e}")
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

@app.route('/getSVG', methods=['GET'])
def get_SVG():
    print(f"checking endpoints: {session['endpoints']}")
    print(f"checking chip_coords: {session['updated_chip_coords']}")
    connections, inputs, outputs = logicanalysis.logic_processing.process_logic(session['endpoints'], session['chip_coords'], datasheets.chip_info, 4.5)
    print(f"generated {connections}")
    expressions = logicanalysis.generate_logic.generate_logic(connections, inputs, outputs, datasheets.chip_info, session['chip_coords'])

    dir = "static/schematics"
    #clear directory
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))
    
    for i, expr in enumerate(expressions):
        logicanalysis.draw_schematic.gen_schematic(expr, i)

    return jsonify(len(expressions))
    

if __name__ == "__main__":
    app.secret_key = "My Secret key"
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True, port=8000)
