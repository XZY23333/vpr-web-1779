import os, cv2
import numpy as np
from constants import *
# from tree_detector import get_tree_mask
# from Project.object_detector_yolov3 import load_net, load_interesting_id_map, get_obj_features
from object_detector_yolov5 import load_model, get_obj_features

# SIFT feature extraction
def extract_sift_features(images):
    sift = cv2.SIFT_create(nfeatures=NO_FEATURES)
    descriptors = []

    for image in images:
        mask = None
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        _, des = sift.detectAndCompute(gray, mask)
        descriptors.append(des)

    return descriptors

# Detect object features using DNN
def extract_obj_features(images, model):
    obj_features = []

    # net = load_net(weight_file_path, cfg_file_path)
    # interesting_id_map = load_interesting_id_map(names_file_path)

    for image in images:
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        features = get_obj_features(rgb, model)
        obj_features.append(features)

    return obj_features

# Feature encoding
def build_features(kmeans, descriptors):
    features = []

    for des in descriptors:
        histogram = np.zeros(len(kmeans.cluster_centers_))
        cluster_result = kmeans.predict(des)

        for i in cluster_result:
            histogram[i] += 1
        features.append(histogram)

    return features

# Dataset info extraction (GSV-Cities dataset)
def load_image_info_list_gsv(dataset_path):
    image_info_list = []

    for city_folder in os.listdir(dataset_path):
        city_folder_path = os.path.join(dataset_path, city_folder)

        for image_file in os.listdir(city_folder_path):
            parts = image_file.split('_')

            if len(parts) > 8:
                parts = parts[:7] + ['_'.join(parts[7:])]

            (city, place_id, year, month, bearing, latitude,
                longitude, panoid) = parts
            panoid = panoid.split('.')[0]

            image_info_list.append({
                K_LABEL: f'{city}_{place_id}',
                K_CITY: city,
                K_PLACEID: place_id,
                K_YEAR: year,
                K_MONTH: month,
                K_BEARING: bearing,
                K_LATITUDE: latitude,
                K_LONGITUDE: longitude,
                K_PANOID: panoid,
                K_FILE: image_file,
                K_PATH: os.path.join(city_folder_path, image_file)
            })

    return image_info_list

# Dataset info extraction
def load_image_info_list(dataset_path):
    image_info_list = []

    for sub_folder in os.listdir(dataset_path):
        sub_folder_path = os.path.join(dataset_path, sub_folder)

        for image_file in os.listdir(sub_folder_path):
            image_info_list.append({
                K_LABEL: sub_folder,
                K_PATH: os.path.join(sub_folder_path, image_file)
            })

    return image_info_list
