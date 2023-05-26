from flask import Flask, request, render_template
import json
from tensorflow import expand_dims
from tensorflow.keras.models import model_from_json
from tensorflow.keras.preprocessing.image import img_to_array
from PIL import Image


flask_app = Flask(__name__)

tf_model = None


def load_tf_model():
    global tf_model

    print('Loading model...')

    model_config = None
    with open('./model/model_config.json') as f:
        model_config = f.read()
    if model_config is None:
        print('error: model_config.json not found')
        exit(-1)

    tf_model = model_from_json(model_config)
    tf_model.load_weights('./model/model_weights').expect_partial()

    print('Model loaded')


def predict_image(img_file):
    image_size = (180, 180)
    img = Image.open(img_file).resize(image_size)
    img_array = img_to_array(img) * 1./255
    img_array = expand_dims(img_array[:, :, :3], 0)  # Create batch axis

    predictions = tf_model.predict(img_array)
    dog_probability = float(predictions[0]) * 100
    cat_probability = 100 - dog_probability

    result = f"This image is {cat_probability:.2f}% cat "
    result += f"and {dog_probability:.2f}% dog."

    return result


@flask_app.route('/', methods=['GET', 'POST'])
def main_route():
    if request.method == 'GET':
        return render_template('index.html')

    if request.form or request.files:
        data = request.form.to_dict()
        img_file = request.files.get('image', None)
        if img_file.filename == '':
            return {
                'error': 'no file provided'
            }

        return predict_image(img_file)

    else:
        if not request.data:
            return {
                'error': 'no input provided'
            }
        data = json.loads(request.data)
    return data


if __name__ == '__main__':
    load_tf_model()

    # listen from any address (0.0.0.0), port 8080
    flask_app.run(host="0.0.0.0", port=8080)
