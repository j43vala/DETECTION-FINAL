import cv2 as cv
import numpy as np
import urllib.request


def calibrate_coordinates(cam_url):
    
    dictionary = cv.aruco.getPredefinedDictionary(cv.aruco.DICT_6X6_250)
    parameters =  cv.aruco.DetectorParameters()
    detector = cv.aruco.ArucoDetector(dictionary, parameters)

    # Detect ArUco markers
    
    while 1:
        img_resp = urllib.request.urlopen(cam_url)
        imgnp = np.array(bytearray(img_resp.read()), dtype=np.uint8)
        img = cv.imdecode(imgnp, -1)
        
        
        gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        corners, ids, rejected = detector.detectMarkers(img)
        if ids is not None and len(ids) == 4:
            marker_coordinates = {5:[250,0],6:[0,0],7:[0,550],8:[250,550]}
            pixel_array = []
            coordinate_array = []
            for i in range(len(ids)):
                # print("\n\nid: ", ids[i])
                # print("corner: \n", corners[i])
                
                marker_center = np.mean(corners[i],axis=1)
                print("\ncenter pixels: ", marker_center[0])
                # print("marker_coordinates: ", marker_coordinates[ids[i][0]])
                
                pixel_array.append(marker_center[0])
                coordinate_array.append(marker_coordinates[ids[i][0]])
                
                pixel_np_array = np.float32(pixel_array)
                coordinate_np_array = np.float32(coordinate_array)
                
            # Draw detected markers on the image
            # print("pixel_array: \n", pixel_np_array)
            # print("coordinate_array: \n", coordinate_np_array)
            perspective_matrix = cv.getPerspectiveTransform(pixel_np_array, coordinate_np_array)
            print("perspective_matrix: \n", perspective_matrix)
            
            #check if matrix is valid
            if perspective_matrix is not None:
                
                coord = cv.perspectiveTransform(pixel_np_array.reshape(1, 4, 2), perspective_matrix)
                # mapped_image = cv.warpPerspective(img, perspective_matrix, (800,600))
                print("coord: ", coord)
            cv.aruco.drawDetectedMarkers(img, corners, ids)
            cv.imshow('calibration', img)
            cv.waitKey(0)
                
            return perspective_matrix

        else:
            print("not enough markers detected...")
            cv.imshow('calibration', img)
            cv.waitKey(1)
            

def get_coordinates(perspective_matrix, pixel_array):
    
    #check if matrix is valid
    if perspective_matrix is not None:
        coord = cv.perspectiveTransform(pixel_array.reshape(1, 4, 2), perspective_matrix)
        # mapped_image = cv.warpPerspective(img, perspective_matrix, (800,600))
        print("coord: ", coord)
    
    return coord
    
    
    
    
    
    
    
    
    
    
    