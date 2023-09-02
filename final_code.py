import urllib.request
import cv2
import numpy as np
import supervision as sv
from ultralytics import YOLO
import os
from services import calibration as cal
from services import detection as det
from services import robo_sim as sim

# Replace the URL with the IP camera's stream URL
url = "http://192.168.1.14:81/"
cam_url = url + "cam-cal.jpg"
# cv2.namedWindow("live Cam Testing", cv2.WINDOW_AUTOSIZE)


model = YOLO(model="best.pt")  # Path to trained model

cap = cv2.VideoCapture(cam_url)
image_name = None

if not cap.isOpened():
    print("Failed to open the IP camera stream")
    exit()

falsh_on = urllib.request.urlopen(url + "flash_on")

perspective_matrix = None




if __name__ == "__main__":
    while True:
        img_resp = urllib.request.urlopen(cam_url)
        imgnp = np.array(bytearray(img_resp.read()), dtype=np.uint8)
        img = cv2.imdecode(imgnp, -1)

        if perspective_matrix is None:
            perspective_matrix = cal.calibrate_coordinates(cam_url)
        
        else:
            corners = det.find_defect(img)  
            print(corners)
            for i in range(len(corners)):
                x1, y1, x2, y2 = corners[i][0], corners[i][1], corners[i][2], corners[i][3]
                
                pixel_array = np.float32([[x1, y1], [x2, y1], [x2, y2], [x1, y2]])
                coordinate_array = cv2.perspectiveTransform(pixel_array.reshape(1, 4, 2), perspective_matrix)[0]
                
                print("coordinate_array: \n", coordinate_array)
                for i,corner_point in enumerate(coordinate_array):
                    # for j,corner_point in enumerate(corner_points):
                        print("corner_point: ", corner_point)
                        coordinate_array[i][0] = round(corner_point[0],1)
                        coordinate_array[i][1] = round(corner_point[1],1)
                        
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                
                top_left_str = str(coordinate_array[0][0]) + "," + str(coordinate_array[0][1])
                cv2.putText(img, top_left_str, (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                
                bottom_right_str = str(coordinate_array[2][0]) + "," + str(coordinate_array[2][1])
                cv2.putText(img, bottom_right_str, (x2, y2), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                # cv2.putText(img, str(coordinate_array[0][3]), (x1, y2), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                
                # draw_box(coordinate_array)
                sim.draw_box(coordinate_array)
            
        # show image
        cv2.imshow("result", img)
        # if not image_name == None:
        #     print("next image_name: ", image_name + "_" + str(count) + ".jpg")

        key = cv2.waitKey(3000)
        if key == ord("q"):
            falsh_off = urllib.request.urlopen(url + "flash_off")
            break
        
        elif key == ord("c"):
            perspective_matrix = cal.calibrate_coordinates(cam_url)
            
            print("perspective matrix: ", perspective_matrix)
            print("calibrated")

        # elif key == ord("n") or image_name == None:
        #     print("new image")
        #     image_name = input("Enter image name: ")
        #     count = 0

        # elif key == ord("s"):
        #     save_image(img, img_name=image_name, count=count)
        #     count += 1
        #     print("saved image: ", image_name + "_" + str(count) + ".jpg")
        
    cap.release()
    cv2.destroyAllWindows()