import cv2
import numpy as np

# Load the image
image = cv2.imread('example-cropped.png')

# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply Gaussian blur to reduce noise
blurred = cv2.GaussianBlur(gray, (7, 7), 1.5)

# Use Hough Circle Transform to detect wells
circles = cv2.HoughCircles(
    blurred, 
    cv2.HOUGH_GRADIENT, 
    dp=1, 
    minDist=30, 
    param1=50, 
    param2=20, 
    minRadius=50, 
    maxRadius=75)

# Function to sort circles top to bottom, then left to right
def sort_circles(circles):
    # First sort by the y-coordinate (top to bottom)
    circles_sorted = sorted(circles, key=lambda c: c[1])
    
    # Now sort each row by the x-coordinate (left to right)
    row_threshold = 40  # Threshold to consider wells in the same row (tune as needed)
    
    rows = []
    current_row = []
    previous_y = circles_sorted[0][1]
    
    for circle in circles_sorted:
        x, y, r = circle
        if abs(y - previous_y) > row_threshold:
            # If the y distance is large, start a new row
            rows.append(sorted(current_row, key=lambda c: c[0]))  # Sort row by x
            current_row = [circle]
            previous_y = y
        else:
            current_row.append(circle)
            previous_y = y
    
    # Add the last row
    if current_row:
        rows.append(sorted(current_row, key=lambda c: c[0]))
    
    # Flatten the rows back into a single list
    sorted_circles = [circle for row in rows for circle in row]
    
    return sorted_circles

# If circles are detected
if circles is not None:
    circles = np.round(circles[0, :]).astype("int")
    sorted_circles = sort_circles(circles)
    
    for i, (x, y, r) in enumerate(sorted_circles):
        # Draw the outer circle
        cv2.circle(image, (x, y), r, (0, 255, 0), 2)  # Green circle with thickness 2
        
        # Draw the center of the circle
        # cv2.circle(image, (x, y), 2, (0, 0, 255), 3)  # Red center dot

        # Create a mask for the current well
        mask = np.zeros_like(gray)
        cv2.circle(mask, (x, y), r, 255, -1)

        # Isolate the region of the current well
        well = cv2.bitwise_and(image, image, mask=mask)

        label = f"Well {i}"
        cv2.putText(image, label, (x - 20, y - r - 10), cv2.FONT_HERSHEY_SIMPLEX, 
                    0.6, (255, 0, 0), 2)  # Blue text above the circle

        # Convert the well region to HSV to detect green
        hsv_well = cv2.cvtColor(well, cv2.COLOR_BGR2HSV)
        lower_green = np.array([35, 40, 40])  # Adjust the lower bound of green
        upper_green = np.array([85, 255, 255])  # Adjust the upper bound of green
        green_mask = cv2.inRange(hsv_well, lower_green, upper_green)

        # Find contours of the green areas (duckweed)
        contours, _ = cv2.findContours(green_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Calculate the total area of duckweed within the well
        total_area = sum(cv2.contourArea(c) for c in contours)
        print(f"Area of duckweed in well {i + 1}: {total_area} pixels")

# Display the result with circles
cv2.imshow("Detected Circles", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
