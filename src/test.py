import os, sys, pickle
import numpy as np
from constants import *
from functions import (
    load_image_info_list_gsv,
    extract_sift_features,
    build_features,
    extract_obj_features
)

def main():
    try:
        image_path = sys.argv[1]
        accuracy_test = os.path.isdir(image_path)
        if len(sys.argv) > 2:
            dnn_flag = True
            obj_weight = float(sys.argv[2])
            yolov5_model = sys.argv[3]
        else:
            dnn_flag = False
    except:
        print('Invalid argv! Expected: test_set_path / test_image')

    print('Load k-means model')

    with open(F_KMEANS, 'rb') as file:
        kmeans = pickle.load(file)

    print('Load classifier model')

    with open(F_CLASSIFIER, 'rb') as file:
        classifier = pickle.load(file)

    if accuracy_test:
        print('Read test set list')

        image_list = load_image_info_list_gsv(os.path.join(image_path, 'test'))
        image_paths = [i[K_PATH] for i in image_list]
    else:
        image_paths = [image_path]

    print('Extract test set SIFT')

    descriptors = extract_sift_features(image_paths)

    print('Build test set features')

    features = build_features(kmeans, descriptors)

    if dnn_flag:
        print('Extract object features using DNN')

        obj_features = extract_obj_features(
            image_paths, yolov5_model, 0.1, 0.45
        )
        features = [
            np.hstack((i * obj_weight, j))
            for i, j in zip(obj_features, features)
        ]

    for i in features:
        print(i)

    print('Predict test set')

    predictions = classifier.predict(features)

    if accuracy_test:
        cnt = 0

        for i in range(len(image_list)):
            label = image_list[i][K_LABEL]
            if label == predictions[i]:
                cnt += 1
            else:
                print(label, predictions[i])

        print('Accuracy: {:.2f}%'.format(100 * cnt / len(image_list)))
    else:
        print('Prediction:', predictions[0])

if __name__ == '__main__':
    main()
