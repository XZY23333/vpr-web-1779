import cv2
import numpy as np

# EXCLUDE_NAMES = set([
#     'person',
#     'bicycle',
#     'motorbike',
#     'car',
#     'bus',
#     'truck',
# ])

INTERESTING_OBJ_LIST = [
    'traffic light',
    'fire hydrant',
    'stop sign',
    'parking meter',
    'bench'
]

def load_net(weight_file_path, cfg_file_path):
    return cv2.dnn.readNet(weight_file_path, cfg_file_path)

# def load_exclude_ids():
#     with open('coco.names', 'r') as file:
#         classes = [line.strip() for line in file.readlines()]
#         exclude_ids = set([i for i in range(len(classes)) if classes[i] in EXCLUDE_NAMES])
#     return exclude_ids

def load_interesting_id_map(names_file_path):
    obj_id_map = {obj:i for i, obj in enumerate(INTERESTING_OBJ_LIST)}
    with open(names_file_path, 'r') as file:
        classes = [line.strip() for line in file.readlines()]
        interesting_id_map = {}
        for i, obj in enumerate(classes):
            if obj in obj_id_map:
                interesting_id_map[i] = obj_id_map[obj]
    return interesting_id_map

def get_obj_features(image, net, interesting_id_map):
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

    height, width, _ = image.shape
    blob = cv2.dnn.blobFromImage(image, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)

    class_ids = []
    confidences = []
    boxes = []

    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if class_id in interesting_id_map:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.1, 0.4)
    
    histogram = np.zeros(len(INTERESTING_OBJ_LIST))

    for i in indices:
        histogram[interesting_id_map[class_ids[i]]] += 1

    return histogram

# def get_obj_mask(image, net, exclude_ids):
#     layer_names = net.getLayerNames()
#     output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

#     height, width, _ = image.shape
#     blob = cv2.dnn.blobFromImage(image, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
#     net.setInput(blob)
#     outs = net.forward(output_layers)

#     class_ids = []
#     confidences = []
#     boxes = []

#     for out in outs:
#         for detection in out:
#             scores = detection[5:]
#             class_id = np.argmax(scores)
#             confidence = scores[class_id]
#             if class_id in exclude_ids and confidence > 0.5:
#                 center_x = int(detection[0] * width)
#                 center_y = int(detection[1] * height)
#                 w = int(detection[2] * width)
#                 h = int(detection[3] * height)
#                 x = int(center_x - w / 2)
#                 y = int(center_y - h / 2)

#                 boxes.append([x, y, w, h])
#                 confidences.append(float(confidence))
#                 class_ids.append(class_id)

#     indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
#     mask = np.ones_like(image[:,:,0]) * 255

#     for i in indices:
#         box = boxes[i]
#         x, y, w, h = box[0], box[1], box[2], box[3]
#         mask[y:y+h, x:x+w] = 0

#     return mask