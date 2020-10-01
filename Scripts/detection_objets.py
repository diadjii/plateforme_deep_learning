import cv2
import numpy as np


class ObjectDetection():
    """docstring for ObjectDetection."""

    def __init__(self, img):
        self.image = img
        self.classes = None
        self.classes_path = "yolo/coco.names"
        self.results = {}
        self.objects = {}

    def get_output_layers(self,net):

        layer_names = net.getLayerNames()

        output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

        return output_layers

    def draw_prediction(self,img, class_id, confidence, x, y, x_plus_w, y_plus_h):

        label = str(self.classes[class_id])

        color = self.COLORS[class_id]

        cv2.rectangle(img, (x,y), (x_plus_w,y_plus_h), color, 2)

        if label in self.objects :
            self.objects[label] = self.objects[label] + 1
        else:
            self.objects[label] = 1

        cv2.putText(img, label, (x-10,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    def detect_objects(self):
        img = cv2.imread(self.image)

        width = img.shape[1]
        height = img.shape[0]
        scale = 0.00392
    
        with open(self.classes_path, 'r') as f:
            self.classes = [line.strip() for line in f.readlines()]

        self.COLORS = np.random.uniform(0, 255, size=(len(self.classes), 3))

        net = cv2.dnn.readNet("yolo/yolov3.cfg", "yolo/yolov3.weights")

        blob = cv2.dnn.blobFromImage(img, scale, (416,416), (0,0,0), True, crop=False)

        net.setInput(blob)

        outs = net.forward(self.get_output_layers(net))

        class_ids = []
        confidences = []
        boxes = []
        conf_threshold = 0.5
        nms_threshold = 0.4

        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5:
                    center_x = int(detection[0] *width)
                    center_y = int(detection[1] * height)

                    w = int(detection[2] *width)
                    h = int(detection[3] * height)
                    x = center_x - w / 2
                    y = center_y - h / 2

                    class_ids.append(class_id)
                    confidences.append(float(confidence))
                    boxes.append([x, y, w, h])

        indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)

        for i in indices:
            i = i[0]
            box = boxes[i]
            x = box[0]
            y = box[1]
            w = box[2]
            h = box[3]

            self.draw_prediction(img, class_ids[i], confidences[i], round(x), round(y), round(x+w), round(y+h))

       
        cv2.imwrite("static/images/object-detection.jpg", img)

        self.results['image'] = 'object-detection.jpg'
        self.results['details'] = self.objects
        
        return True