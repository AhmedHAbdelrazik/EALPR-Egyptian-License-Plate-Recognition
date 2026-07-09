from plate_detector import detect_plate
from char_detector import detect_characters
from char_classifier import classify_characters

def run_pipeline(image):
    
    plate_results = detect_plate(image)
    
    char_results, plate_crop = detect_characters(image, plate_results)
    
    
    char_boxes = sorted(char_results[0].boxes, key=lambda b: b.xyxy[0][0])
    
    
    plate_width = plate_crop.shape[1]
    mid = plate_width / 2
    
    left_chars = []   
    right_chars = []  
    
    for char_box in char_boxes:
        x1, y1, x2, y2 = map(int, char_box.xyxy[0])
        char_crop = plate_crop[y1:y2, x1:x2]
        label, conf = classify_characters(char_crop)
        
        center_x = (x1 + x2) / 2
        if center_x < mid:
            left_chars.append(label)
        else:
            right_chars.append(label)
    
    
    plate_text = "".join(right_chars) + " | " + "".join(left_chars)
    return plate_text

print(run_pipeline(r"C:\projects\EALPR_Project\0048.jpg"))


