# pyrefly: ignore [missing-import]
from ultralytics import YOLO
# pyrefly: ignore [missing-import]
import cv2

model = YOLO("C:\projects\EALPR_Project\models\cracter_classfication_model.pt")
print(model.info())


def detect_characters(image_path, plate_results):
    
    original_image = cv2.imread(image_path)    
    box = plate_results[0].boxes[0].xyxy[0]
    x1, y1, x2, y2 = map(int, box)
    plate_crop = original_image[y1:y2, x1:x2]

    model = YOLO("models/chracter_detection_model.pt")
    results = model(plate_crop)
    return results, plate_crop

