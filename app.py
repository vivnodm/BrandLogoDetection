from flask import Flask, render_template, request,jsonify, Response
import detect_object
import os.path
from detector import *
from detect_object import *
import traceback
import shutil
import json

app = Flask(__name__)

@app.route("/upload", methods=['POST'])
def upload():
    path_to_video = request.json['video_path']
    blur_decision = request.json['blur_decision']
    ext = os.path.splitext(path_to_video)[-1].lower()
    if os.path.exists(path_to_video):
        if ext in ('.mp4', '.avi', '.mp4v'):
            with open("video_meta.json", "w") as outfile:
                outfile.write(json.dumps(dict(path_to_video=path_to_video, blur_decision=blur_decision)))

            data = {'message': "Video Found Successfully!!, Click on Detect to Detect logo's"}
            return jsonify(data),200
    else:
        data = {'message': 'Video Upload Unsuccessful, Please Provide a Proper Path'}
        return jsonify(data),400

# @app.route('/video_feed')
# def video_feed():
#     detector_obj = DetectorTF2()
#     video_path = './video_dir/tosend.mp4'
#     return Response(DetectFromVideo(detector_obj, video_path, True ), mimetype='multipart/x-mixed-replace; boundary=frame')

# @app.route('/')
# def index():
#     """Video streaming home page."""
#     return render_template('index.html')

@app.route("/detect", methods=['GET'])
def detect():
    try:
        video_object = {}
        with open('video_meta.json', 'r') as openfile:
            video_object = json.load(openfile)
        if video_object == {}: raise Exception("Video Not Found!!!")
        video_path = video_object['path_to_video']
        blur_decision = video_object['blur_decision']
        detector_obj = DetectorTF2()
        return Response(DetectFromVideo(detector_obj, video_path, blur_decision), mimetype='multipart/x-mixed-replace; boundary=frame')
        
    except Exception as e:
        print(e)
        traceback.print_exc()
        data = {'message':'Error Occurred'}
        return jsonify(data),400

@app.route("/frequency", methods=['GET'])
def frequency():
    try:
        freq_object = {}
        with open('freq_meta.json', 'r') as openfile:
            freq_object = json.load(openfile)
        if freq_object == {}: raise Exception("Frequency Not Found!!")

        return freq_object

    except Exception as e:
        print(e)
        traceback.print_exc()
        data = {'message':'Error Occurred'}
        return jsonify(data),400

if __name__=='__main__':
    app.run()
