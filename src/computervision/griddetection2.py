import cv2 
import numpy as np 
from matplotlib import pyplot as plt 

# Reading the image
img = cv2.imread('src/images/breadboard6.jpg')

# Converting the image to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Applying a Gaussian blur to reduce noise and smooth the image
blurred = cv2.GaussianBlur(gray, (7, 7), 0)  # Adjust the kernel size for more/less blur

# Applying a binary threshold to the blurred grayscale image
_, threshold = cv2.threshold(blurred, 150, 255, cv2.THRESH_BINARY)

# Finding contours in the thresholded image
contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Variable to store the largest contour
largest_contour = None
max_area = 0

# Looping through the detected contours to find the largest one by area
for contour in contours:
    area = cv2.contourArea(contour)
    if area > max_area:
        max_area = area
        largest_contour = contour

# If a largest contour was found, proceed to approximate its shape
if largest_contour is not None:
    # Approximating the largest contour shape to get corner points
    epsilon = 0.02 * cv2.arcLength(largest_contour, True)  # Approximation precision
    approx = cv2.approxPolyDP(largest_contour, epsilon, True)

    # Drawing the contour and corners if it has 4 points
    if len(approx) == 4:
        cv2.drawContours(img, [approx], -1, (0, 255, 0), 5)  # Draw the rectangle with green color
        
        # Draw each corner of the rectangle
        for point in approx:
            x, y = point[0]  # Each point is an array of arrays
            cv2.circle(img, (x, y), 8, (255, 0, 0), -1)  # Draw blue circles at corners
            cv2.putText(img, f"({x}, {y})", (x+10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

# Displaying the image with the detected rectangle corners
cv2.imshow('Rectangle Corners', img)

cv2.waitKey(0)
cv2.destroyAllWindows()
