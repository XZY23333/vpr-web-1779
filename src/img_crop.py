import cv2
import os
import sys

def resize_image(image, target_size=(640, 480)):
    h, w = image.shape[:2]
    scale = max(target_size[0] / w, target_size[1] / h)

    resized_image = cv2.resize(image, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)

    h, w = resized_image.shape[:2]
    startx = w//2 - target_size[0]//2
    starty = h//2 - target_size[1]//2

    return resized_image[starty:starty+target_size[1], startx:startx+target_size[0]]

def resize_and_copy_image(image_path, input_folder, output_folder, target_size=(640, 480)):
    image = cv2.imread(image_path)
    if image is None:
        print(f"Can't load image: {image_path}")
        return

    cropped_image = resize_image(image, target_size)

    relative_path = os.path.relpath(image_path, input_folder)
    output_subfolder = os.path.join(output_folder, os.path.dirname(relative_path))
    os.makedirs(output_subfolder, exist_ok=True)

    filename = os.path.basename(image_path)
    output_path = os.path.join(output_subfolder, filename)
    cv2.imwrite(output_path, cropped_image)
    print(f"Proceed: {output_path}")

def process_folder(input_folder, output_folder):
    for root, _, files in os.walk(input_folder):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_path = os.path.join(root, file)
                resize_and_copy_image(image_path, input_folder, output_folder)

def main(input_folder, output_folder):
    process_folder(input_folder, output_folder)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <input_folder> <output_folder>")
        sys.exit(1)

    main(sys.argv[1], sys.argv[2])
