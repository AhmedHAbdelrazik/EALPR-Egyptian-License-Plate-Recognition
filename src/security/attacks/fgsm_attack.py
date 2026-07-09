# pyrefly: ignore [missing-import]
from ultralytics import YOLO
import yaml
import shutil
# pyrefly: ignore [missing-import]
import cv2
# pyrefly: ignore [missing-import]
import numpy as np
import os


def apply_adversarial_noise(image, epsilon):
    # Apply FGSM-like adversarial noise to an image
    if epsilon == 0:
        return image

    # Convert to float (0 to 1)
    img_float = image.astype(np.float32) / 255.0

    # Generate uniform noise simulating FGSM effect
    noise = np.random.uniform(-epsilon, epsilon, img_float.shape)

    # Add noise and clip values
    adv_img = img_float + noise
    adv_img = np.clip(adv_img, 0, 1)

    # Convert back to uint8 (0 to 255)
    return (adv_img * 255).astype(np.uint8)


def evaluate_fgsm(model_path, dataset_yaml, epsilons=[0.0, 0.05, 0.1, 0.2, 0.3, 0.4]):

    model = YOLO(model_path)
    results_list = []

    print("🧪 Starting FGSM Adversarial Evaluation...")

    for eps in epsilons:
        print(f"\n[~] Testing Epsilon: {eps}")

        # Create temp folder for noisy images
        temp_dir = "temp_fgsm/images/val"
        if os.path.exists("temp_fgsm"):
            shutil.rmtree("temp_fgsm")
        os.makedirs(temp_dir, exist_ok=True)

        # Load original val images path from yaml
        with open(dataset_yaml, 'r') as f:
            data = yaml.safe_load(f)
        val_images_path = os.path.join(data['path'], data['val'])

        # Copy labels
        labels_src = val_images_path.replace("images", "labels")
        labels_dst = "temp_fgsm/labels/val"
        if os.path.exists(labels_src):
            shutil.copytree(labels_src, labels_dst)

        # Apply noise to all val images
        for img_name in os.listdir(val_images_path):
            if img_name.endswith(('.jpg', '.png', '.jpeg')):
                img = cv2.imread(os.path.join(val_images_path, img_name))
                noisy_img = apply_adversarial_noise(img, eps)
                cv2.imwrite(os.path.join(temp_dir, img_name), noisy_img)

        # Create temp yaml
        temp_yaml_content = {
            'path': os.path.abspath("temp_fgsm"),
            'train': 'images/val',
            'val': 'images/val',
            'nc': len(model.names),
            'names': model.names
        }
        with open('temp_fgsm.yaml', 'w') as f:
            yaml.dump(temp_yaml_content, f)

        # Evaluate
        metrics = model.val(data='temp_fgsm.yaml', split='val', conf=0.5, imgsz=640, verbose=False)
        map50 = metrics.results_dict['metrics/mAP50(B)']

        results_list.append({"Epsilon": eps, "mAP50": round(map50, 4)})
        print(f"✅ Epsilon {eps} | mAP50: {map50:.4f}")

    # Cleanup
    if os.path.exists("temp_fgsm"):
        shutil.rmtree("temp_fgsm")
    if os.path.exists("temp_fgsm.yaml"):
        os.remove("temp_fgsm.yaml")

    print("\n" + "="*40)
    print("FGSM ATTACK RESULTS")
    for r in results_list:
        print(f"Epsilon {r['Epsilon']} → mAP50: {r['mAP50']}")
    print("="*40)

    return results_list


