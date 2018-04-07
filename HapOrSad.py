import numpy as np
from keras import layers
from keras.layers import Input, Dense, Activation, ZeroPadding2D, BatchNormalization, Flatten, Conv2D
from keras.layers import AveragePooling2D, MaxPooling2D, Dropout, GlobalMaxPooling2D, GlobalAveragePooling2D
from keras.models import Model
from keras.preprocessing import image
from keras.utils import layer_utils
from keras.utils.data_utils import get_file
from keras.applications.imagenet_utils import preprocess_input
import pydot
from IPython.display import SVG
from keras.utils.vis_utils import model_to_dot
from keras.utils import plot_model
from keras.models import load_model
from kt_utils import *

import keras.backend as K
K.set_image_data_format('channels_last')

from flask import Flask, render_template, request
app = Flask(__name__)
import os

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

form = """
<form id="upload-form" action="/upload" method="POST" enctype="multipart/form-data">
  <input type="file" name="file" accept="image/*" multiple>
  <input type="submit" value="send">
</form>
"""

@app.route("/")
def index():
    return form

@app.route("/upload", methods=['POST'])
def upload():
    target = os.path.join(APP_ROOT, 'static/')
    print(target)

    if not os.path.isdir(target):
        os.mkdir(target)
    print("hi")
    for file in request.files.getlist("file"):
        print("hi")
        print(file)
        filename = file.filename
        destination = "/".join([target, filename])
        print(destination)
        file.save(destination)
    happyModel = load_model("happyModel.h5")
    img = image.load_img(destination, target_size=(64, 64))
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = img / 255
    print(happyModel.predict(img))
    if happyModel.predict(img)[0][0] > 0.82:
        return render_template("Happy.html", image_name=filename)
    else:
        return render_template("Sad.html", image_name=filename)

if __name__ == "__main__":
    app.run(port=4555, debug=True)





