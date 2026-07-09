# pyrefly: ignore [missing-import]
from ultralytics import YOLO
# pyrefly: ignore [missing-import]
import torch
import os

def apply_weight_tampering(model_path, output_path, intensity=0.1):
    if not os.path.exists(model_path):
        print(f"❌ File not found: {model_path}")
        return False

    try:
        print("--- Applying Weight Tampering Attack ---")

        checkpoint = torch.load(model_path, map_location='cpu', weights_only=False)

        # Extract model weights
        if isinstance(checkpoint, dict) and 'model' in checkpoint:
            model_data = checkpoint['model']
            state_dict = model_data.state_dict() if hasattr(model_data, 'state_dict') else model_data
        else:
            state_dict = checkpoint

        # Add noise to weights
        for key in state_dict.keys():
            if 'weight' in key:
                noise = torch.randn_like(state_dict[key]) * intensity
                state_dict[key] += noise

        # Save tampered model
        torch.save(checkpoint, output_path)
        print(f"✅ Success! Tampered model saved at: {output_path}")
        return True

    except Exception as e:
        print(f"❌ Attack failed: {e}")
        return False


def evaluate_tampering(original_path, tampered_path, dataset_yaml):

    print("⏳ Evaluating Original Model...")
    model_orig = YOLO(original_path)
    res_orig = model_orig.val(data=dataset_yaml, split='val', imgsz=640, verbose=False)
    mAP_orig = res_orig.results_dict['metrics/mAP50(B)']

    print("⏳ Evaluating Tampered Model...")
    model_tamp = YOLO(tampered_path)
    res_tamp = model_tamp.val(data=dataset_yaml, split='val', imgsz=640, verbose=False)
    mAP_tamp = res_tamp.results_dict['metrics/mAP50(B)']

    drop = ((mAP_orig - mAP_tamp) / mAP_orig) * 100

    print("\n" + "="*40)
    print(f"Original Model mAP50:  {mAP_orig:.4f}")
    print(f"Tampered Model mAP50:  {mAP_tamp:.4f}")
    print(f"Performance Drop:      {drop:.2f}%")
    print("="*40)

    return mAP_orig, mAP_tamp, drop
