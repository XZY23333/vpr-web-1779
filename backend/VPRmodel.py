import pickle
import numpy as np
from constants import *
from functions import (
    extract_sift_features,
    build_features,
    extract_obj_features
)
from object_detector_yolov5 import load_model

class VPRmodel:
    def __init__(self, dnn_flag, obj_weight, yolov5_model):
        self.dnn_flag = dnn_flag
        self.obj_weight = obj_weight
        self.yolov5_model = yolov5_model

        with open(F_KMEANS, 'rb') as file:
            self.kmeans = pickle.load(file)

        with open(F_CLASSIFIER, 'rb') as file:
            self.classifier = pickle.load(file)

        self.dnn_model = load_model(yolov5_model, 0.25, 0.45)
    
    def predict(self, image):
        descriptors = extract_sift_features([image])
        features = build_features(self.kmeans, descriptors)

        if self.dnn_flag:
            obj_features = extract_obj_features(
                [image], self.dnn_model
            )
            features = [
                np.hstack((i * self.obj_weight, j))
                for i, j in zip(obj_features, features)
            ]

        predictions = self.classifier.predict(features)

        return predictions[0]
