import os
import cv2
from flask import Flask, request, jsonify
import numpy as np
import requests

app = Flask(__name__)

@app.route('/process', methods=['POST'])
def process_images():
    # Define YOLOv3 model paths
    MODEL_WEIGHTS_URL = 'https://pjreddie.com/media/files/yolov3.weights'
    MODEL_CFG_URL = 'https://github.com/pjreddie/darknet/blob/master/cfg/yolov3.cfg?raw=true'
    MODEL_WEIGHTS_PATH = 'yolov3.weights'
    MODEL_CFG_PATH = 'yolov3.cfg'

    # Download YOLOv3 model files if they don't exist
    if not os.path.exists(MODEL_WEIGHTS_PATH):
        response = requests.get(MODEL_WEIGHTS_URL)
        with open(MODEL_WEIGHTS_PATH, 'wb') as f:
            f.write(response.content)

    if not os.path.exists(MODEL_CFG_PATH):
        response = requests.get(MODEL_CFG_URL)
        with open(MODEL_CFG_PATH, 'wb') as f:
            f.write(response.content)

    # Load YOLOv3 model
    net = cv2.dnn.readNet(MODEL_WEIGHTS_PATH, MODEL_CFG_PATH)

    # Get output layer names
    layer_names = net.getLayerNames()
    output_layer_indices = net.getUnconnectedOutLayers()
    output_layers = [layer_names[i - 1] for i in output_layer_indices]

    # Get uploaded images from request
    uploaded_images = request.files.getlist('images')

    # Function to process uploaded images
    def process_images(uploaded_images):
        # Initialize dictionary to store vehicle counts for each image
        vehicle_counts = {}

        # Loop over all uploaded images
        for i, img_bytes in enumerate(uploaded_images):
            # Convert bytes to numpy array
            nparr = np.frombuffer(img_bytes.read(), np.uint8)

            # Read image from numpy array
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            img = cv2.resize(img, None, fx=0.4, fy=0.4)
            height, width, channels = img.shape

            # Detect objects
            blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
            net.setInput(blob)
            outs = net.forward(output_layers)

            # Initialize vehicle count
            vehicle_count = 0

            # Loop over each detection
            for out in outs:
                for detection in out:
                    scores = detection[5:]
                    class_id = np.argmax(scores)
                    confidence = scores[class_id]
                    if confidence > 0.5:
                        # Object detected
                        center_x, center_y, w, h = (detection[0:4] * np.array([width, height, width, height])).astype('int')

                        # Check if the object is a vehicle (class IDs corresponding to vehicles in the COCO dataset)
                        if class_id in [2, 3, 5, 7]:
                            vehicle_count += 1

            # Store vehicle count for this image
            vehicle_counts[f"Image {i+1}"] = vehicle_count

        # Sort the dictionary by vehicle count in descending order
        sorted_counts = sorted(vehicle_counts.items(), key=lambda x: x[1], reverse=True)

        # Construct output string
        output_string = ""
        for img_name, count in sorted_counts:
            output_string += f"{img_name}: {count}\n"

        return output_string

    # Process uploaded images
    result = process_images(uploaded_images)

    return result

if __name__ == '__main__':
    app.run(debug=True)
