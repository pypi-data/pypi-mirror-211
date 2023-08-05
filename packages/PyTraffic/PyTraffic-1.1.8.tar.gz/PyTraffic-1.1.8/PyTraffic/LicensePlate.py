# PyTraffic - License Plate

''' This is the "LicensePlate" module. '''

# Imports
import os
import cv2
import imutils
import numpy as np
import pytesseract
import mimetypes

# The Directory
directory = os.path.dirname(os.path.realpath(__file__)).replace(os.sep, "/")

# OpenCV Cascade Classifier (Plate)
plate_cascade = cv2.CascadeClassifier(directory + "/models/haarcascade_russian_plate_number.xml")

# Sample Media
SampleImage1 = directory + "/sample_media/LicensePlate/images/1.jpg"
SampleImage2 = directory + "/sample_media/LicensePlate/images/2.jpg"
SampleImage3 = directory + "/sample_media/LicensePlate/images/3.jpg"
SampleImage4 = directory + "/sample_media/LicensePlate/images/4.jpg"
SampleImage5 = directory + "/sample_media/LicensePlate/images/5.jpg"
SampleImage6 = directory + "/sample_media/LicensePlate/images/6.jpg"
SampleImage7 = directory + "/sample_media/LicensePlate/images/7.jpg"
SampleImage8 = directory + "/sample_media/LicensePlate/images/8.jpg"

# Function 1 - Get License Plate
def getLicensePlate(imagePath, show=False):
    # Variables
    tesseractPath = None

    # Checking for Tesseract
    if (os.path.exists("C:/Program Files/Tesseract-OCR/tesseract.exe")):
        tesseractPath = "C:/Program Files/Tesseract-OCR/tesseract.exe"
    elif (os.path.exists("C:/Program Files (x86)/Tesseract-OCR/tesseract.exe")):
        tesseractPath = "C:/Program Files (x86)/Tesseract-OCR/tesseract.exe"
    else:
        tesseractPath = None

    # Checking if Path Exists
    if (os.path.exists(imagePath)):
        # Checking for Tesseract
        if (tesseractPath != None):
            # Checking the File Type
            mimetypes.init()

            mimestart = mimetypes.guess_type(imagePath)[0]
            mimestart = mimestart.split("/")[0]

            if (mimestart == "image"): # Image:
                # Connecting to Tesseract
                pytesseract.pytesseract.tesseract_cmd = tesseractPath

                # Reading the Image
                img = cv2.imread(imagePath, cv2.IMREAD_COLOR)
                img = cv2.resize(img, (600,400))

                # Converting the Image to Grayscale
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
                gray = cv2.bilateralFilter(gray, 13, 15, 15) 

                # Finding & Counting Contours
                edged = cv2.Canny(gray, 30, 200) 
                contours = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                contours = imutils.grab_contours(contours)
                contours = sorted(contours, key = cv2.contourArea, reverse = True)[:10]
                screenCnt = None

                for c in contours:
                    peri = cv2.arcLength(c, True)
                    approx = cv2.approxPolyDP(c, 0.018 * peri, True)

                    if len(approx) == 4:
                        screenCnt = approx
                        break

                if screenCnt is None:
                    detected = 0
                else:
                    detected = 1

                if detected == 1:
                    cv2.drawContours(img, [screenCnt], -1, (0, 0, 255), 3)

                mask = np.zeros(gray.shape, np.uint8)
                new_image = cv2.drawContours(mask, [screenCnt], 0,255, -1,)
                new_image = cv2.bitwise_and(img, img, mask=mask)

                (x, y) = np.where(mask == 255)
                (topx, topy) = (np.min(x), np.min(y))
                (bottomx, bottomy) = (np.max(x), np.max(y))
                Cropped = gray[topx:bottomx+1, topy:bottomy+1]

                # License Plate Number
                text = pytesseract.image_to_string(Cropped, config="--psm 11")

                # Stopping OpenCV
                cv2.waitKey(0)
                cv2.destroyAllWindows()

                # Check for "show" Argument
                if (show):
                    # Reading the Image
                    img = cv2.imread(imagePath)

                    # Converting the Images to Grayscale
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

                    # Finding the Plates
                    plates = plate_cascade.detectMultiScale(gray, 1.2, 5)

                    # Displaying Each License Plate
                    for (x,y,w,h) in plates:
                        cv2.rectangle(img, (x,y), (x+w, y+h), (0,255,0), 2)
                        gray_plates = gray[y:y+h, x:x+w]
                        color_plates = img[y:y+h, x:x+w]

                        cv2.imshow("Vehicle Image", img)
                        cv2.imshow("Number Plate", gray_plates)
                        cv2.waitKey(0)

                # Returning the License Plate Number
                return text
            else:
                raise Exception("The file provided must be an image.")
        else:
            raise Exception("Make sure Tesseract-OCR is installed and you haven't changed the installation directory. Install Tesseract-OCR with the default installation settings.")
    else:
        raise Exception("The image file path does not exist.")