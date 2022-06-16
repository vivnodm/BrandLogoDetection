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
    # frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    # frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    # out = cv2.VideoWriter('logo_detected_video.mp4', cv2.VideoWriter_fourcc(*"mp4v"), 30, (frame_width, frame_height))

    while (cap.isOpened()):
        ret, img = cap.read()
        if not ret: break

        timestamp1 = time.time()
        det_boxes = detector.DetectFromImage(img)
        elapsed_time = round((time.time() - timestamp1) * 1000)  # ms
        response = detector.DisplayDetections(img, det_boxes,blur_decision=blur_decision, det_time=elapsed_time)
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
        
        # out.write(img)

    cap.release()
    # out.release()
    logo_dict = { key: int(value//fps) for key,value in logo_dict.items()}

    with open("freq_meta.json", "w") as outfile:
        outfile.write(json.dumps(dict(summary=logo_dict)))


