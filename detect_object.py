import os
import cv2
import time
import argparse
import json
from detector import DetectorTF2


def DetectFromVideo(detector,Video_path, blur_decision=False):
    logo_dict = {}
    cap = cv2.VideoCapture(Video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)

    while (cap.isOpened()):
        ret, img = cap.read()
        if not ret: break

        det_boxes = detector.DetectFromImage(img)
        response = detector.DisplayDetections(img, det_boxes,blur_decision=blur_decision)
        frame = response["image"]
        logo_set = response["logo_set"]

        for logo in logo_set:
            if logo not in logo_dict:
                logo_dict[logo] = 1
            else:
                logo_dict[logo] += 1

        retrieve, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()
    for key,value in logo_dict.items():
        if (value//fps)!=0:
            logo_dict[key]=int(value//fps)
        else:
            logo_dict[key] = 1

    with open("freq_meta.json", "w") as outfile:
        outfile.write(json.dumps(dict(summary=logo_dict)))


