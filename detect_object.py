import os
import cv2
import time
import argparse

from detector import DetectorTF2


def DetectFromVideo(detector,Video_path, blur_decision=False):
    logo_dict = {}
    cap = cv2.VideoCapture(Video_path)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter('logo_detected_video.mp4', cv2.VideoWriter_fourcc(*"mp4v"), 30, (frame_width, frame_height))

    while (cap.isOpened()):
        ret, img = cap.read()
        if not ret: break

        timestamp1 = time.time()
        det_boxes = detector.DetectFromImage(img)
        elapsed_time = round((time.time() - timestamp1) * 1000)  # ms
        response = detector.DisplayDetections(img, det_boxes,blur_decision=blur_decision, det_time=elapsed_time)
        img = response["image"]
        logo_set = response["logo_set"]
        #cv2.imshow('TF2 Detection', img)

        for logo in logo_set:
            if logo not in logo_dict:
                logo_dict[logo] = 1
            else:
                logo_dict[logo] += 1
        out.write(img)

    cap.release()
    out.release()

    return logo_dict

