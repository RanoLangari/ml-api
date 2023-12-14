import os
import numpy as np
from tensorflow import keras
from keras.preprocessing import image
from keras.models import load_model
from flask import Flask, request, jsonify



app = Flask(__name__)
app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg'])
app.config['UPLOAD_FOLDER'] = 'static/upload'
model = load_model('ktp_detection_model.h5')



@app.route('/predict', methods=['POST'])
def predict():
    imgFIle = request.files['image']
    img_path = os.path.join(app.config['UPLOAD_FOLDER'], imgFIle.filename)
    imgFIle.save(img_path)
    img = image.load_img(img_path, target_size=(150, 150))  
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    predictions = model.predict(img_array)
    os.remove(img_path)
    score = predictions[0]
    if score < 0.5:
        return jsonify({'status': 'success', 'result': 'KTP', 'score': str(score[0])})
    else:
        return jsonify({'status': 'success', 'result': 'Bukan KTP', 'score': str(score[0])})
    
    
if __name__ == '__main__':
    app.run(debug=True, port=5000)
    
    