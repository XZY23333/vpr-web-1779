import os, sys, shutil, random
from constants import *

def load_image_info_list(dataset_path):
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

def main():
    try:
        lower_bound = int(sys.argv[1])
        image_path = sys.argv[2]
        output_path = sys.argv[3]
        size = int(sys.argv[4])
        cities = set(sys.argv[5:])
    except:
        print("Invalid argv! Expected: lower_bound, image_path, output_path, top_num, cities...")
        exit(0)

    img_list = load_image_info_list(image_path)

    if not os.path.exists(output_path):
        os.makedirs(output_path)
    else:
        shutil.rmtree(output_path)

    if not os.path.exists(os.path.join(output_path, 'training')):
        os.makedirs(os.path.join(output_path, 'training'))

    if not os.path.exists(os.path.join(output_path, 'test')):
        os.makedirs(os.path.join(output_path, 'test'))

    img_cnt = {}

    for i in img_list:
        if i[K_CITY] not in cities:
            continue
        label = f'{i[K_CITY]}_{i[K_PLACEID]}'
        if label not in img_cnt:
            img_cnt[label] = 0
        img_cnt[label] += 1

    # selected = sorted(img_cnt, key=img_cnt.get, reverse=True)

    selected = [i for i in img_cnt if img_cnt[i] >= lower_bound]
    random.shuffle(selected)
    selected = set(selected[:min(size, len(selected))])

    print('Actual number of cities:', len(selected))

    img_list = [i for i in img_list if f'{i[K_CITY]}_{i[K_PLACEID]}' in selected]
    random.shuffle(img_list)

    visit = set()

    for i in img_list:
        label = f'{i[K_CITY]}_{i[K_PLACEID]}'
        if label not in visit:
            visit.add(label)
            cat = 'test'
        else:
            cat = 'training'
        city_folder = os.path.join(output_path, cat, i[K_CITY])
        if not os.path.exists(city_folder):
            os.makedirs(city_folder)
        shutil.copy(i[K_PATH], os.path.join(city_folder, i[K_FILE]))

    print('Avg img count:', len(img_list) / len(visit))

if __name__ == '__main__':
    main()
