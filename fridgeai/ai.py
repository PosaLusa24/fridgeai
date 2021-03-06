import os
import numpy as np
import tensorflow as tf
import json


def predict(images):
    model_path = os.path.join('data', [
        file for file in os.listdir('data')
        if os.path.splitext(file)[1] == '.tflite'
    ][0])
    # Load the TFLite model and allocate tensors.
    interpreter = tf.lite.Interpreter(model_path=model_path)

    # Get input and output tensors.
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    interpreter.resize_tensor_input(
        input_details[0]['index'], [len(images), 32, 32, 3])
    interpreter.allocate_tensors()

    data = np.array(images, dtype=np.float32) / 255.0
    interpreter.set_tensor(input_details[0]['index'], data)

    interpreter.invoke()

    # The function `get_tensor()` returns a copy of the tensor data.
    # Use `tensor()` in order to get a pointer to the tensor.
    output_data = interpreter.get_tensor(output_details[0]['index'])
    prediction = np.argmax(np.bincount(output_data.argmax(axis=1)))
    with open(os.path.join('data', 'labels.json'), 'rb') as file:
        item_list = json.load(file)
    return item_list[prediction]


"""
from os import path
import numpy as np
from keras.models import load_model


def predict(images):
    data = np.array(images).astype("float") / 255.0
    model = load_model(path.join(".", "data"))
    preds = model.predict(data, batch_size=32).argmax(axis=1)
    print(preds)
    prediction = np.argmax(np.bincount(preds))

    if prediction == 0:
        prediction = "Coke"
    elif prediction == 1:
        prediction = "Emborg"
    elif prediction == 2:
        prediction = "Pepsi"

    return prediction
"""
