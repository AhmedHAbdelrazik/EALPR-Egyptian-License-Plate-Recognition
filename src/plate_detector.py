# pyrefly: ignore [missing-import]
from ultralytics import YOLO


model = YOLO("C:\projects\EALPR_Project\models\plate_detection_model.pt")
print(model.info())


def detect_plate(image):
    model = YOLO("C:\projects\EALPR_Project\models\plate_detection_model.pt") 
    results = model(image)
    return results

