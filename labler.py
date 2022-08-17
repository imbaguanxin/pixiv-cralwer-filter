import os
from tqdm import tqdm
import cv2
import shutil

img_extensions = ['jpg', 'jpeg', 'png', 'bmp', 'tif']


def filter_images(path):
    result = []
    for file in os.listdir(path):
        extension = file[file.rfind(".") + 1:].lower()
        if extension in img_extensions:
            result.append(file)
    return result


def label(img_path, dest_path):
    if not os.path.exists(img_path):
        print(f"image path not found: {img_path}")
    img_files = filter_images(img_path)
    if not os.path.exists(dest_path):
        os.mkdir(dest_path)
    if 'true' not in os.listdir(dest_path):
        os.mkdir(os.path.join(dest_path, 'true'))
    if 'false' not in os.listdir(dest_path):
        os.mkdir(os.path.join(dest_path, 'false'))
    
    img_files.sort()
    for img_file in tqdm(img_files, desc="Image Labeling"):
        if img_file in os.listdir(os.path.join(dest_path, "true")) or \
                img_file in os.listdir(os.path.join(dest_path, "false")):
            continue
        file_path = os.path.join(img_path, img_file)
        img = cv2.imread(file_path)
        cv2.imshow("labeling image", img)
        key = cv2.waitKey(0)
        # 32 = space, if not space, means good image
        # press space to place image in false folder
        if key != 32:
            shutil.copyfile(file_path, os.path.join(dest_path, "true", img_file))
        else:
            shutil.copyfile(file_path, os.path.join(dest_path, "false", img_file))


if __name__ == '__main__':
    label("image/20220709-week", "image/label_result")
