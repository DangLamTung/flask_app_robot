#!/usr/bin/env python
# __author__ = "Ronie Martinez"
# __copyright__ = "Copyright 2019, Ronie Martinez"
# __credits__ = ["Ronie Martinez"]
# __license__ = "MIT"
# __maintainer__ = "Ronie Martinez"
# __email__ = "ronmarti18@gmail.com"
import json
import random
import time
from datetime import datetime
import cv2
from flask import Flask, Response, render_template

application = Flask(__name__)
random.seed()  # Initialize the random number generator

camera = cv2.VideoCapture("video.avi")
@application.route('/')
def index():
    return render_template('index.html')


@application.route('/chart-data')
def chart_data():
    def generate_random_data():
        while True:
            json_data = json.dumps(
                {'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'value': random.random() * 100})
            yield f"data:{json_data}\n\n"
            time.sleep(0.1)

    return Response(generate_random_data(), mimetype='text/event-stream')
def gen():  
    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            # ret, buffer = cv2.imencode('.jpg', frame)
            # frame = buffer.tobytes()
            cv2.imwrite('demo.jpg', frame)
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + open('demo.jpg', 'rb').read() + b'\r\n')


@application.route('/video_feed')
def video_feed():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    application.run(debug=True, threaded=True)
