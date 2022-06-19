import cv2
import numpy as np
import tensorflow as tf
from object_detection.utils import label_map_util
from PIL import Image, ImageFilter
import config
import traceback

class DetectorTF2:

    def __init__(self, path_to_checkpoint = config.path_to_checkpoint, path_to_labelmap = config.path_to_labelmap):
        self.class_id = None
        self.Threshold = 0.5
        # Loading label map
        label_map = label_map_util.load_labelmap(path_to_labelmap)
        categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=config.max_num_classes,
                                                                    use_display_name=True)
        self.category_index = label_map_util.create_category_index(categories)

        tf.keras.backend.clear_session()
        self.detect_fn = tf.saved_model.load(path_to_checkpoint)

    def DetectFromImage(self, img):
        im_height, im_width, _ = img.shape
        # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
        input_tensor = np.expand_dims(img, 0)
        detections = self.detect_fn(input_tensor)

        bboxes = detections['detection_boxes'][0].numpy()
        bclasses = detections['detection_classes'][0].numpy().astype(np.int32)
        bscores = detections['detection_scores'][0].numpy()
        det_boxes = self.ExtractBBoxes(bboxes, bclasses, bscores, im_width, im_height)

        return det_boxes

    def ExtractBBoxes(self, bboxes, bclasses, bscores, im_width, im_height):
        bbox = []
        for idx in range(len(bboxes)):
            if self.class_id is None or bclasses[idx] in self.class_id:
                if bscores[idx] >= self.Threshold:
                    y_min = int(bboxes[idx][0] * im_height)
                    x_min = int(bboxes[idx][1] * im_width)
                    y_max = int(bboxes[idx][2] * im_height)
                    x_max = int(bboxes[idx][3] * im_width)
                    class_label = self.category_index[int(bclasses[idx])]['name']
                    bbox.append([x_min, y_min, x_max, y_max, class_label, float(bscores[idx])])
        return bbox

    def DisplayDetections(self, image, boxes_list,blur_decision):
        try:
            if not boxes_list: 
                return {"image":image, "logo_set":set()}  # input list is empty
            img = image.copy()
            logo_set = set()
            for idx in range(len(boxes_list)):
                x_min = boxes_list[idx][0]
                y_min = boxes_list[idx][1]
                x_max = boxes_list[idx][2]
                y_max = boxes_list[idx][3]
                cls = str(boxes_list[idx][4])
                logo_set.add(cls)
                score = str(np.round(boxes_list[idx][-1], 2))

                text = cls + " : " + score
                blur_img = None
                if blur_decision==True:
                    image_rgb  = Image.fromarray(img.astype('uint8'), 'RGB')
                    cropped_img= image_rgb.crop((x_min,y_max,x_max,y_min))
                    blurred_image = Image.new("RGB", (x_max-x_min, y_max-y_min), (255, 255, 255)) #cropped_img.filter(ImageFilter.)
                    image_rgb.paste(blurred_image, box=(x_min,y_min))
                    blur_img = np.array(image_rgb)
                if blur_img is not None: img = blur_img
                cv2.rectangle(img, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
                cv2.rectangle(img, (x_min, y_min - 20), (x_min, y_min), (255, 255, 255), -1)
                cv2.putText(img, text, (x_min + 5, y_min - 7), cv2.FONT_HERSHEY_TRIPLEX, 0.5, (255, 255, 255), 2)

            return {"image":img, "logo_set":logo_set}
        except Exception as e :
            traceback.print_exc()
            print(e)
