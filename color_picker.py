import cv2
import numpy as np

# Load the image
image = cv2.imread('images/start_r1_plate1_2.jpg')

# Function to capture mouse click events and print HSV values
def pick_color(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        # Get the BGR color from the image at the clicked point
        bgr_color = image[y, x]
        
        # Convert BGR to HSV
        hsv_color = cv2.cvtColor(np.uint8([[bgr_color]]), cv2.COLOR_BGR2HSV)[0][0]
        
        # Print the picked color in both BGR and HSV
        print(f"Clicked at: ({x}, {y})")
        print(f"BGR Color: {bgr_color}")
        print(f"HSV Color: {hsv_color}")
        
        # Draw a circle at the clicked point for visual feedback
        cv2.circle(image, (x, y), 5, (0, 0, 255), 2)
        cv2.imshow("Pick a color", image)

# Display the image and set the mouse callback for color picking
cv2.imshow("Pick a color", image)
cv2.setMouseCallback("Pick a color", pick_color)

cv2.waitKey(0)
cv2.destroyAllWindows()
