from ultralytics import YOLO
import supervision as sv
import cv2 as cv

model = YOLO(model="best.pt") # Path to trained model


def find_defect(img):
    
  print("\n\nfinding results")
  
  result = model.predict([img], imgsz=640, verbose=False)[0]
  # print("\nresult: \n", result)
  detections = sv.Detections.from_ultralytics(result)
#   print("\ndetections: \n", detections) 
  # x1, y1, x2, y2 = detections.xyxy # topleft corner, bottom right corner
  # cls_id = detections.class_id # class id i.e. 0 in this case
  # score = detections.confidences # probability score
  

  box_annotators = sv.BoxAnnotator()

  # render_img = box_annotators.annotate(img, detections)

#   cv.imshow("defect", render_img)
  return detections.xyxy
