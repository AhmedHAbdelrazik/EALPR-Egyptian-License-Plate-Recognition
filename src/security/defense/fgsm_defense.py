# pyrefly: ignore [missing-import]
from ultralytics import YOLO
# pyrefly: ignore [missing-import]
import cv2
import os
import shutil
import yaml
# pyrefly: ignore [missing-import]
import numpy as np


def denoise_image(image):
    # Apply Gaussian + Median filters to suppress FGSM noise
    gaussian = cv2.GaussianBlur(image, (3, 3), 0)
    cleaned = cv2.medianBlur(gaussian, 3)
    return cleaned


def defend_single_image(image):
    # Apply denoising defense on a single image (numpy array)
    return denoise_image(image)


def evaluate_fgsm_defense(model_path, poisoned_images_dir, dataset_yaml):

    model = YOLO(model_path)

    # Load dataset info
    with open(dataset_yaml, 'r') as f:
        data = yaml.safe_load(f)

    # Create defended dataset folder
    defended_dir = "temp_defended"
    defended_img_path = f"{defended_dir}/images/val"

    if os.path.exists(defended_dir):
        shutil.rmtree(defended_dir)
    os.makedirs(defended_img_path, exist_ok=True)

    # Copy labels
    labels_src = os.path.join(data['path'], "labels/val")
    if os.path.exists(labels_src):
        shutil.copytree(labels_src, f"{defended_dir}/labels/val")

    # Apply denoising to all poisoned images
    print("🧼 Applying Denoising Defense...")
    for img_name in os.listdir(poisoned_images_dir):
        if img_name.endswith(('.jpg', '.png', '.jpeg')):
            img = cv2.imread(os.path.join(poisoned_images_dir, img_name))
            if img is not None:
                cleaned = denoise_image(img)
                cv2.imwrite(os.path.join(defended_img_path, img_name), cleaned)

    # Create temp yaml
    defended_yaml = {
        'path': os.path.abspath(defended_dir),
        'train': 'images/val',
        'val': 'images/val',
        'nc': len(model.names),
        'names': model.names
    }
    with open('temp_defended.yaml', 'w') as f:
        yaml.dump(defended_yaml, f)

    # Evaluate
    print("🔍 Evaluating Defended Dataset...")
    metrics = model.val(data='temp_defended.yaml', split='val', conf=0.5, imgsz=640, verbose=False)
    recovered_map = metrics.results_dict['metrics/mAP50(B)'] * 100

    # Known values from attack evaluation
    baseline_map = 99.26
    attack_map = 38.32

    print("\n" + "="*40)
    print("FGSM DEFENSE RESULTS")
    print(f"Baseline Clean Model:      {baseline_map:.2f}%")
    print(f"Under FGSM Attack (0.40):  {attack_map:.2f}%")
    print(f"After Denoising Defense:   {recovered_map:.2f}%")
    print("="*40)

    # Cleanup
    if os.path.exists(defended_dir):
        shutil.rmtree(defended_dir)
    if os.path.exists('temp_defended.yaml'):
        os.remove('temp_defended.yaml')

    return baseline_map, attack_map, recovered_map