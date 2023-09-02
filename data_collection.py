import urllib.request
import cv2
import numpy as np
import supervision as sv
from ultralytics import YOLO
import os

# Replace the URL with the IP camera's stream URL
url = "http://192.168.1.14:81/"
cam_url = url + "cam-cal.jpg"
folder_name = "fabric_defects/"
# cv2.namedWindow("live Cam Testing", cv2.WINDOW_AUTOSIZE)

falsh_on = urllib.request.urlopen(url + "flash_on")

model = YOLO(model="best.pt")  # Path to trained model

cap = cv2.VideoCapture(cam_url)
image_name = None

if not cap.isOpened():
      print("Failed to open the IP camera stream")
      exit()


def save_image(img, img_name, save_path="data/", count=0):
      # create folder if not exist
      if not os.path.exists(save_path):
            os.makedirs(save_path)
            
      # save image
      cv2.imwrite(save_path + img_name + str(count) +".jpg", img)
      print("saved image: ", img_name + "_"+ str(count) +".jpg")


while True:
      img_resp = urllib.request.urlopen(cam_url)
      imgnp = np.array(bytearray(img_resp.read()), dtype=np.uint8)
      img = cv2.imdecode(imgnp, -1)
      
      # show image
      cv2.imshow("result", img)
      if not image_name == None:
            print("next image_name: ", image_name + "_"+ str(count) +".jpg")
      

      key = cv2.waitKey(1)
      if key == ord("q"):
            falsh_off = urllib.request.urlopen(url + "flash_off")
            break
      
      elif key == ord("n") or image_name == None:
            print("new image")
            image_name = input("Enter image name: ")
            count = 0

      elif key == ord("s"):
            save_image(img, img_name=image_name,save_path=folder_name,count = count)
            count += 1
            print("saved image: ", image_name + "_"+ str(count) +".jpg")
