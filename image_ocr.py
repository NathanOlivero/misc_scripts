import cv2
import numpy
import pytesseract

#Define tesseract exe call
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

# get grayscale image
def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# noise removal
def remove_noise(image):
    return cv2.medianBlur(image,5)

#thresholding
def thresholding(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

#dilation
def dilate(image):
    kernel = numpy.ones((5,5),numpy.uint8)
    return cv2.dilate(image, kernel, iterations = 1)

#erosion
def erode(image):
    kernel = numpy.ones((5,5),numpy.uint8)
    return cv2.erode(image, kernel, iterations = 1)

#opening - erosion followed by dilation
def opening(image):
    kernel = numpy.ones((5,5),numpy.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

#canny edge detection
def canny(image):
    return cv2.Canny(image, 100, 200)

#skew correction
def deskew(image):
    coords = numpy.column_stack(numpy.where(image > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated

#template matching
def match_template(image, template):
    return cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)

def flood_fill(image):
    img_greyscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Threshold.
    # Set values equal to or above 220 to 0.
    # Set values below 220 to 255.
    threshold, img_threshold = cv2.threshold(img_greyscale, 220, 255, cv2.THRESH_BINARY_INV);
    # Copy the thresholded image.
    img_floodfill = img_threshold.copy()
    # Mask used to flood filling.
    # Notice the size needs to be 2 pixels than the image.
    h, w = img_threshold.shape[:2]
    mask = numpy.zeros((h+2, w+2), numpy.uint8)
    # Floodfill from point (0, 0)
    cv2.floodFill(img_floodfill, mask, (0,0), 255);
    return img_floodfill

#imgFilePath = "C:\\Users\\Nathan\\Documents\\Code\\Python\\images\\traffic_info_sign.jpg"
imgFilePath = "C:\\Users\\Nathan\\Documents\\Code\\Python\\images\\grocery_receipt.jpeg"
img = cv2.imread(imgFilePath)
img = get_grayscale(img)
cv2.imshow("Processed Image", img)

# Adding custom options
custom_config = r'--oem 3 --psm 6'
resultOCR = pytesseract.image_to_string(img, config=custom_config)
print(resultOCR)
cv2.waitKey(0)
