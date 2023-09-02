import urllib.request
import cv2
import numpy as np
import supervision as sv
from ultralytics import YOLO
from datetime import datetime


# Replace the URL with the IP camera's stream URL
url = 'http://192.168.1.14:81/'
cam_url = url + "cam-cal.jpg"
# cv2.namedWindow("live Cam Testing", cv2.WINDOW_AUTOSIZE)

falsh_on = urllib.request.urlopen(url + "flash_on")


model = YOLO(model="best.pt") # Path to trained model


cap = cv2.VideoCapture(cam_url)

if not cap.isOpened():
    print("Failed to open the IP camera stream")
    exit()

def find_adapter(img): 
  print("\n\nfinding results")
  
  result = model.predict([img], imgsz=640, verbose=False)[0]
  # print("\nresult: \n", result)
  detections = sv.Detections.from_ultralytics(result)
  print("\ndetections: \n", detections) 
  # x1, y1, x2, y2 = detections.xyxy # topleft corner, bottom right corner
  # cls_id = detections.class_id # class id i.e. 0 in this case
  # score = detections.confidences # probability score
  

  box_annotators = sv.BoxAnnotator()

  render_img = box_annotators.annotate(img, detections)

  cv2.imshow("result", render_img)




start_time = datetime.now()

#  main loop starts here
while True:
  img_resp = urllib.request.urlopen(cam_url)
  imgnp = np.array(bytearray(img_resp.read()), dtype=np.uint8)
  img = cv2.imdecode(imgnp, -1)
  find_adapter(img)
 
  key = cv2.waitKey(1)
  if key == ord('q'):
        break
