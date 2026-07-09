# pyrefly: ignore [missing-import]
from ultralytics import YOLO
# pyrefly: ignore [missing-import]
import cv2
import os
# pyrefly: ignore [missing-import]
import numpy as np


def apply_trigger(image, label_path):
    # Add white square trigger to image based on plate location
    with open(label_path, 'r') as f:
        lines = f.readlines()

    if not lines:
        return image, False

    data = lines[0].split()
    x_c, y_c, w, h = map(float, data[1:])
    img_h, img_w, _ = image.shape

    px = int((x_c - w/2) * img_w)
    py = int((y_c - h/2) * img_h)

    # Draw white 20x20 trigger square
    cv2.rectangle(image, (px, py), (px+20, py+20), (255, 255, 255), -1)
    return image, True


def apply_backdoor_trigger(image_path, label_path, output_path):
    # Apply trigger to a single image and save it
    img = cv2.imread(image_path)
    if img is None:
        print(f"❌ Image not found: {image_path}")
        return False

    poisoned_img, success = apply_trigger(img, label_path)

    if success:
        cv2.imwrite(output_path, poisoned_img)
        print(f"✅ Trigger applied and saved at: {output_path}")
        return True
    else:
        print("❌ Failed to apply trigger.")
        return False


def evaluate_backdoor(original_model_path, backdoor_model_path, clean_yaml, poisoned_yaml):
    

    print("⏳ Evaluating on Clean Data...")
    model = YOLO(backdoor_model_path)
    res_clean = model.val(data=clean_yaml, split='val', imgsz=640, verbose=False)
    mAP_clean = res_clean.results_dict['metrics/mAP50(B)']

    print("⏳ Evaluating on Poisoned Data...")
    res_poison = model.val(data=poisoned_yaml, split='val', imgsz=640, verbose=False)
    mAP_poison = res_poison.results_dict['metrics/mAP50(B)']

    attack_impact = ((mAP_clean - mAP_poison) / mAP_clean) * 100

    print("\n" + "="*50)
    print("BACKDOOR ATTACK RESULTS")
    print(f"Clean Data  mAP50:   {mAP_clean:.4f}")
    print(f"Poisoned Data mAP50: {mAP_poison:.4f}")
    print(f"Attack Impact:       {attack_impact:.2f}%")
    print("="*50)

    return mAP_clean, mAP_poison, attack_impact
