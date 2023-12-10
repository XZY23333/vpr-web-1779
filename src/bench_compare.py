import subprocess, os, shutil
from time import time
import numpy as np

LOWER_BOUND = 10
NO_TEST = 100
WEIGHTS = [10]
SIZES = [50, 100, 200]
CITIES = ['London Boston Chicago Osaka']

def main():
    bench_data = os.path.join('dataset', 'bench')
    source_data = os.path.join('dataset', 'Images')

    accuracy_rec_base = []
    training_time_rec_base = []
    test_time_rec_base = []

    accuracy_rec_dnn = []
    training_time_rec_dnn = []
    test_time_rec_dnn = []

    for size in SIZES:
        accuracy_base = []
        training_time_base = []
        test_time_base = []

        accuracy_dnn = [[] for _ in range(len(WEIGHTS))]
        training_time_dnn = [[] for _ in range(len(WEIGHTS))]
        test_time_dnn = [[] for _ in range(len(WEIGHTS))]

        for i in range(1, NO_TEST + 1):
            print(f'(size = {size}) #{i}: Generating dataset')

            subprocess.run(f'python3 data_extractor.py {LOWER_BOUND} {source_data} {bench_data} {size} {" ".join(CITIES)}', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            print(f'(size = {size}, NO DNN) #{i}: Training')

            training_time = time()
            subprocess.run(f'python3 training.py {bench_data}', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            training_time = time() - training_time

            print(f'(size = {size}, NO DNN) #{i}: Testing')

            test_time = time()
            result = subprocess.run(f'python3 test.py {bench_data}', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            test_time = time() - test_time

            accuracy = float(result.stdout.split(' ')[-1].strip()[:-1])

            accuracy_base.append(accuracy)
            training_time_base.append(training_time)
            test_time_base.append(test_time)

            print(f'(size = {size}, NO DNN) #{i}: Accracy = {accuracy}%, Training time = {training_time}, Test time = {test_time}')

            for j, weight in enumerate(WEIGHTS):
                print(f'(size = {size}, weight = {weight}) #{i}: Training')

                training_time = time()
                subprocess.run(f'python3 training.py {bench_data} {weight} yolov5x', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                training_time = time() - training_time

                print(f'(size = {size}, weight = {weight}) #{i}: Testing')

                test_time = time()
                result = subprocess.run(f'python3 test.py {bench_data} {weight} yolov5x', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                test_time = time() - test_time

                accuracy = float(result.stdout.split(' ')[-1].strip()[:-1])

                accuracy_dnn[j].append(accuracy)
                training_time_dnn[j].append(training_time)
                test_time_dnn[j].append(test_time)

                print(f'(size = {size}, weight = {weight}) #{i}: Accracy = {accuracy}%, Training time = {training_time}, Test time = {test_time}')
    
        accuracy_rec_base.append(accuracy_base)
        training_time_rec_base.append(training_time_base)
        test_time_rec_base.append(test_time_base)

        accuracy_rec_dnn.append(accuracy_dnn)
        training_time_rec_dnn.append(training_time_dnn)
        test_time_rec_dnn.append(test_time_dnn)

    if os.path.exists(bench_data):
        shutil.rmtree(bench_data)

    print('Benchmark complete! Result:')

    print('Average Accuracy:')
    print('Size\tNo DNN', end='')

    for weight in WEIGHTS:
        print(f'\t{weight}', end='')
    
    print('')

    for i, size in enumerate(SIZES):
        print(f'{size}\t{np.mean(accuracy_rec_base[i])}', end='')
        for j in range(len(WEIGHTS)):
            print(f'\t{np.mean(accuracy_rec_dnn[i][j])}', end='')
        print('')
    
    print('')

    print('Average training time:')
    print('Size\tNo DNN', end='')

    for weight in WEIGHTS:
        print(f'\t{weight}', end='')
    
    print('')

    for i, size in enumerate(SIZES):
        print(f'{size}\t{np.mean(training_time_rec_base[i])}', end='')
        for j in range(len(WEIGHTS)):
            print(f'\t{np.mean(training_time_rec_dnn[i][j])}', end='')
        print('')
    
    print('')

    print('Average test time:')
    print('Size\tNo DNN', end='')

    for weight in WEIGHTS:
        print(f'\t{weight}', end='')
    
    print('')

    for i, size in enumerate(SIZES):
        print(f'{size}\t{np.mean(test_time_rec_base[i])}', end='')
        for j in range(len(WEIGHTS)):
            print(f'\t{np.mean(test_time_rec_dnn[i][j])}', end='')
        print('')
    
    print('')


if __name__ == '__main__':
    main()
