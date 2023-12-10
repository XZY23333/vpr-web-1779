import torch
import numpy as np

OBJ_LIST = [
    'traffic light',
    'fire hydrant',
    'stop sign',
    'parking meter',
    'bench'
]

def load_model(yolov5_model, conf_thres, iou_thres):
    model = torch.hub.load('ultralytics/yolov5', yolov5_model, pretrained=True)
    model.conf = conf_thres
    model.iou = iou_thres

    for obj in OBJ_LIST:
        assert obj in model.names.values(), f'Object {obj} is not in model.names!'

    return model

def get_obj_features(image, model):
    results = model(image)
    obj_map = {obj:i for i, obj in enumerate(OBJ_LIST)}
    histogram = np.zeros(len(OBJ_LIST))

    for item in results.xyxy[0]:
        # x1, y1, x2, y2, conf, cls_id = item
        _, _, _, _, _, cls_id = item
        class_name = model.names[int(cls_id)]
        if class_name in OBJ_LIST:
            histogram[obj_map[class_name]] += 1

    return histogram
