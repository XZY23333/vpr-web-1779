import os, sys, pickle
import numpy as np
from sklearn.svm import SVC
# from sklearn.ensemble import RandomForestClassifier
from constants import *
from functions import (
    load_image_info_list_gsv,
    load_image_info_list,
    extract_sift_features,
    build_features,
    extract_obj_features
)

# from sklearn.cluster import KMeans
from cuml.cluster import KMeans

# Vocabulary building
def build_vocabulary(descriptors, k):
    kmeans = KMeans(n_clusters=k, random_state=0, n_init=3, tol=1e-4)
    kmeans.fit(np.vstack(descriptors))

    return kmeans

# Classifier training
def train_classifier(features, labels):
    classifier = SVC(kernel='linear')
    # classifier = RandomForestClassifier(n_estimators=1000)
    classifier.fit(features, labels)

    return classifier

def main():
    try:
        image_path = sys.argv[1]
        if len(sys.argv) > 2:
            dnn_flag = True
            obj_weight = float(sys.argv[2])
            yolov5_model = sys.argv[3]
        else:
            dnn_flag = False
    except:
        print('Invalid argv! Expected: training_set_path')

    print('Read training set list')

    # training_list = load_image_info_list_gsv(os.path.join(image_path, 'training'))
    training_list = load_image_info_list(image_path)
    image_paths = [i[K_PATH] for i in training_list]

    print(f'Training size: {len(training_list)}')

    descriptors = extract_sift_features(image_paths)
    sift_size = 0

    for i in range(len(descriptors)):
        if descriptors[i] is None:
            print('Error: no features were found in', training_list[i][K_FILE])
            exit(0)
        sift_size += len(descriptors[i])

    print('SIFT size: {}'.format(sift_size))
    print('Build vocabulary')

    kmeans = build_vocabulary(descriptors,k=NO_CLUSTERS)

    with open(F_KMEANS, 'wb') as file:
        pickle.dump(kmeans, file)

    print('Build features')

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

    print('Train classifier')

    labels = [i[K_LABEL] for i in training_list]
    classifier = train_classifier(features, labels)

    with open(F_CLASSIFIER, 'wb') as file:
        pickle.dump(classifier, file)

    print('Training completed')

if __name__ == '__main__':
    main()
