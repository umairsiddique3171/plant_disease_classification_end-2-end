import os
import json
import cv2
import numpy as np
import tensorflow as tf
import streamlit as st

import warnings
warnings.filterwarnings("ignore")


# loading the trained model
model = tf.keras.models.load_model("model.h5")

# loading class names
class_indices = json.load(open("class_indices.json","r"))

# classification func
def classify(img,model,class_indices,target_size=(256,256)):
    img = cv2.resize(img,target_size)
    img_array = np.array(img)
    img_array = np.expand_dims(img_array,axis=0)
    img_array = img_array.astype('float32')/255.
    predictions = model.predict(img_array)
    predicted_class_index = np.argmax(predictions,axis=1)[0]
    predicted_class_name = class_indices[str(predicted_class_index)]
    return predicted_class_name

# Streamlit App
st.title('🍃 Plant Disease Classification')

file = st.file_uploader("Upload an image...", type=["jpg", "jpeg", "png"])

if file is not None: 
    file_bytes = np.asarray(bytearray(file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, 1)
    col1, col2 = st.columns(2)

    with col1:
        resized_img = cv2.resize(img,(256, 256))
        st.image(resized_img,use_column_width=True)

    with col2:
        if st.button('Classify'):
            classification = classify(img,model,class_indices)
            st.success(f'### {str(classification)}')
