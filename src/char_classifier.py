# pyrefly: ignore [missing-import]
from ultralytics import YOLO


model = YOLO("C:\projects\EALPR_Project\models\cracter_classfication_model.pt")
print(model.info())


def classify_characters(char_crop):
    model = YOLO("C:\projects\EALPR_Project\models\cracter_classfication_model.pt")
    results = model.predict(char_crop, imgsz=96, verbose=False)[0]
    
    idx = int(results.probs.top1)       
    label = results.names[idx]           
    conf = float(results.probs.top1conf) 
    
    return label, conf

