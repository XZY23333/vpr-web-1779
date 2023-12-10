import subprocess, os, shutil
from time import time

LOWER_BOUND = 10
NO_TEST = 20
SIZES = [50, 100]
CITIES = ['London Boston Chicago Osaka']

def main():
    bench_data = os.path.join('dataset', 'bench')
    source_data = os.path.join('dataset', 'Images')

    avg_accuracy = []
    avg_training_time = []
    avg_test_time = []

    for size in SIZES:
        total_accuracy = 0
        total_training_time = 0
        total_test_time = 0

        for i in range(1, NO_TEST + 1):
            print(f'(size = {size}) #{i}: Generating dataset')

            subprocess.run(f'python3 data_extractor.py {LOWER_BOUND} {source_data} {bench_data} {size} {" ".join(CITIES)}', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            print(f'(size = {size}) #{i}: Training')

            training_time = time()
            subprocess.run(f'python3 training.py {bench_data}', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            training_time = time() - training_time

            print(f'(size = {size}) #{i}: Testing')

            test_time = time()
            result = subprocess.run(f'python3 test.py {bench_data}', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            test_time = time() - test_time

            accuracy = float(result.stdout.split(' ')[-1].strip()[:-1])
            total_accuracy += accuracy
            total_training_time += training_time
            total_test_time += test_time

            print(f'(size = {size}) #{i}: Accracy = {accuracy}%, Training time = {training_time}, Test time = {test_time}')
        
        avg_accuracy.append(total_accuracy / NO_TEST)
        avg_training_time.append(total_training_time / NO_TEST)
        avg_test_time.append(total_test_time / NO_TEST)

    if os.path.exists(bench_data):
        shutil.rmtree(bench_data)

    print('Benchmark complete! Result:')

    for i in range(len(SIZES)):
        print(f'Size = {SIZES[i]}, Average accuracy = {avg_accuracy[i]}%, Average training time = {avg_training_time[i]}, Average test time = {avg_test_time[i]}')

if __name__ == '__main__':
    main()
