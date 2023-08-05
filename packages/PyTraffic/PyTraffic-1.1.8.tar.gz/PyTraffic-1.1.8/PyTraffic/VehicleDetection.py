# PyTraffic - Vehicle Detection

''' This is the "VehicleDetection" module. '''

# Imports
from PIL import Image
import cv2
import numpy as np
import os
import mimetypes
import time

# The Directory
directory = os.path.dirname(os.path.realpath(__file__)).replace(os.sep, "/")

# OpenCV Cascade Classifier (Car)
car_cascade = cv2.CascadeClassifier(directory + "/models/haarcascade_car.xml")

# Sample Media
SampleImage1 = directory + "/sample_media/VehicleDetection/images/1.jpg"
SampleImage2 = directory + "/sample_media/VehicleDetection/images/2.jpg"
SampleImage3 = directory + "/sample_media/VehicleDetection/images/3.jpg"
SampleImage4 = directory + "/sample_media/VehicleDetection/images/4.jpg"
SampleImage5 = directory + "/sample_media/VehicleDetection/images/5.jpg"
SampleImage6 = directory + "/sample_media/VehicleDetection/images/6.jpg"
SampleImage7 = directory + "/sample_media/VehicleDetection/images/7.jpg"
SampleImage8 = directory + "/sample_media/VehicleDetection/images/8.jpg"
SampleImage9 = directory + "/sample_media/VehicleDetection/images/9.jpg"
SampleImage10 = directory + "/sample_media/VehicleDetection/images/10.jpg"

SampleVideo1 = directory + "/sample_media/VehicleDetection/videos/1.mp4"

# Function 1 - Detect Cars
def detectCars(path, show=False):
    # Checking if Path Exists
    if (os.path.exists(path)):
        # Checking the File Type
        mimetypes.init()

        mimestart = mimetypes.guess_type(path)[0]
        mimestart = mimestart.split("/")[0]

        if (mimestart == "image"): # Image
            # Opening the Image
            image = Image.open(path)
            image = image.resize((450, 250))
            image_arr = np.array(image)

            # Converting Image to Greyscale
            grey = cv2.cvtColor(image_arr, cv2.COLOR_BGR2GRAY)
            Image.fromarray(grey)

            # Blurring the Image
            blur = cv2.GaussianBlur(grey, (5,5), 0)
            Image.fromarray(blur)

            # Dilating the Image
            dilated = cv2.dilate(blur, np.ones((3,3)))
            Image.fromarray(dilated)

            # Morphology
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))
            closing = cv2.morphologyEx(dilated, cv2.MORPH_CLOSE, kernel) 
            Image.fromarray(closing)

            # Identifying the Cars
            cars = car_cascade.detectMultiScale(closing, 1.1, 1)

            # Counting the Cars
            count = 0

            for (x, y, w, h) in cars:
                cv2.rectangle(image_arr,(x,y),(x+w,y+h),(255,0,0),2)
                count += 1

            # Returning the Image
            if (show):
                cv2.imshow("Vehicle Detection - Cars", image_arr)
                cv2.waitKey(0)

            # Returning the Count
            return count
        elif (mimestart == "video"): # Video
            # Opening the Video
            video = cv2.VideoCapture(path)

            # Opening the Video and Processing
            while video.isOpened():
                time.sleep(.05)

                # Reading the First Frame
                ret, frame = video.read()
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                # Identifying the Cars
                cars = car_cascade.detectMultiScale(gray, 1.4, 2)

                for (x,y,w,h) in cars:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 255), 2)
                    cv2.imshow("Vehicle Detection - Cars", frame)

                # Clicking "q" Closes the Video
                if cv2.waitKey(1) == ord("q"):
                    break

            # Stopping OpenCV
            video.release()
            cv2.destroyAllWindows()
        else:
            raise Exception("The file provided must be an image or a video.")
    else:
        raise Exception("The image or video file path does not exist.")