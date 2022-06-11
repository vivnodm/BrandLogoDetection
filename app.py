from flask import Flask, render_template, request,jsonify
import detect_object
from flask_ngrok import run_with_ngrok
import os.path
from detector import *
from detect_object import *
import traceback
import shutil

app = Flask(__name__)

@app.route("/upload", methods=['POST'])
def upload():
    path_to_video = request.json['video_path']
    ext = os.path.splitext(path_to_video)[-1].lower()
    print(ext)
    if os.path.exists(path_to_video):
        # check for video extension
         if ext in ('.mp4', '.avi', '.mp4v'):
            # add json message instead flash
            data = {'message': "Video Found Successfully!!, Click on Detect to Detect logo's"}
            return jsonify(data),200
            #flash('Video Found Successfully!!, Click on Detect to Detect logo\'s')
    else:
        data = {'message': 'Video Upload Unsuccessful, Please Provide a Proper Path'}
        return jsonify(data),404



@app.route("/detect", methods=['POST'])
def detect():
    video_path = request.json['video_path']
    blur_decision = request.json['blur_decision']
    detector_obj = DetectorTF2()

    try:

        logo_list = DetectFromVideo(detector_obj, video_path, blur_decision)
        output__video_path = os.path.join(os.path.dirname(__file__),'logo_detected_video.mp4')
        save_video_path = os.path.join(os.path.dirname(video_path),'logo_detected_video.mp4')
        shutil.move(output__video_path, save_video_path)

        data = {'path':save_video_path,'summary':logo_list}
        return jsonify(data),200
    except Exception as e:
        print(e)
        traceback.print_exc()
        data = {'message':'Error Occurred'}
        return jsonify(data),404


if __name__=='__main__':
    app.run()
