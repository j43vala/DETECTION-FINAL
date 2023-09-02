import cv2
import urllib.request
import numpy as np


from datetime import datetime, timedelta


# Replace the URL with the IP camera's stream URL
url = 'http://192.168.1.14:81/'
cam_url = url + "cam-cal.jpg"
cv2.namedWindow("live Cam Testing", cv2.WINDOW_AUTOSIZE)

falsh_on = urllib.request.urlopen(url + "flash_on")

# # Load the ArUco dictionary
# aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)

# # Create an ArUco marker detector
# aruco_params = cv2.aruco.DetectorParameters()

dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
parameters =  cv2.aruco.DetectorParameters()
detector = cv2.aruco.ArucoDetector(dictionary, parameters)

# Create a VideoCapture object
cap = cv2.VideoCapture(cam_url)
start_time = datetime.now()
# Check if the IP camera stream is opened successfully
if not cap.isOpened():
    print("Failed to open the IP camera stream")
    exit()

def calibrate_coordinates(img):
    print("\n\n\n")
    # Detect ArUco markers
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # negated_img = cv2.bitwise_not(img)
    corners, ids, rejected = detector.detectMarkers(img)
    # corners, ids, rejected = detector.detectMarkers(img)
    

    
        
    if ids is not None and len(ids) == 4:
        marker_coordinates = {5:[25,0],6:[0,0],7:[0,55],8:[25,55]}
        pixel_array = []
        coordinate_array = []
        for i in range(len(ids)):
            # print("\n\nid: ", ids[i])
            # print("corner: \n", corners[i])
            
            marker_center = np.mean(corners[i],axis=1)
            # print("\ncenter pixels: ", marker_center[0])
            # print("marker_coordinates: ", marker_coordinates[ids[i][0]])
            
            pixel_array.append(marker_center[0])
            coordinate_array.append(marker_coordinates[ids[i][0]])
            # pixel_array = [
            #     [50,0],
            #     [150,0],
            #     [200,200],
            #     [0,200]
            # ]
            # coordinate_array = [
            #     [0,0],
            #     [200,0],
            #     [200,200],
            #     [0,200]
            # ]
            pixel_np_array = np.float32(pixel_array)
            coordinate_np_array = np.float32(coordinate_array)
            
        # Draw detected markers on the image
        # print("pixel_array: \n", pixel_np_array)
        print("coordinate_array: \n", coordinate_np_array)
        perspective_matrix = cv2.getPerspectiveTransform(pixel_np_array, coordinate_np_array)
        print("perspective_matrix: \n", perspective_matrix)
        
        #check if matrix is valid
        if perspective_matrix is not None:
            point_to_transform = pixel_np_array[0]
            print(pixel_np_array.shape)
            coord = cv2.perspectiveTransform(pixel_np_array.reshape(1, 4, 2), perspective_matrix)
            # mapped_image = cv2.warpPerspective(img, perspective_matrix, (800,600))
            print("coord: ", coord)

    cv2.aruco.drawDetectedMarkers(img, corners, ids)
    cv2.imshow('live Cam Testing', img)

# Read and display video frames
while True:
    img_resp = urllib.request.urlopen(cam_url)
    imgnp = np.array(bytearray(img_resp.read()), dtype=np.uint8)
    im = cv2.imdecode(imgnp, -1)

    calibrate_coordinates(im)
    print("time: ", datetime.now() - start_time)
    start_time = datetime.now()
    
    key = cv2.waitKey(5)
    if key == ord('q'):
        break

# cap.release()
# cv2.destroyAllWindows()


    # find pixels and map pixels of coordinates

    # create perspective trnsform matrix

# cv2.imshow('live Cam Testing',img)
    # time.sleep(3)

    # return matrix


# calibrat_coordinates(image)

# # Read and display video frames
# while True:
#     # Read a frame from the video stream
#     img_resp=urllib.request.urlopen(url)
#     imgnp=np.array(bytearray(img_resp.read()),dtype=np.uint8)
#     #ret, frame = cap.read()
#     im = cv2.imdecode(imgnp,-1)
    
#     calibrat_coordinates(im)

#     # cv2.imshow('live Cam Testing',im)
#     key=cv2.waitKey(5)
#     if key==ord('q'):
#         break
falsh_off = urllib.request.urlopen(url + "flash_off")
# time.sleep(3)

cap.release()
cv2.destroyAllWindows()