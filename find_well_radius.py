import math
import cv2

# Load the image
image = cv2.imread('Pilot Week 3 Day 7 Plate 1-2.jpg')

# Store the clicked points
points = []

# Function to capture mouse click events
def draw_circle(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        points.append((x, y))
        print(f"Clicked at: ({x}, {y})")
        
        # Draw the clicked point as a small red circle
        cv2.circle(image, (x, y), 2, (0, 0, 255), 2)
        cv2.imshow("Measure Wells", image)

        # If two points are clicked (center and edge)
        if len(points) == 2:
            x1, y1 = points[0]
            x2, y2 = points[1]

            # Calculate the radius (distance between points)
            radius = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
            print(f"Radius: {radius} pixels")

            # Draw a line between the two points
            cv2.line(image, points[0], points[1], (255, 0, 0), 2)

            # Label the line with the length in pixels
            midpoint = ((x1 + x2) // 2, (y1 + y2) // 2)
            cv2.putText(image, f"{radius:.2f} px", midpoint, cv2.FONT_HERSHEY_SIMPLEX, 
                        0.7, (255, 255, 255), 2)

            # Show the updated image with the line and label
            cv2.imshow("Measure Wells", image)

# Display the image and set the mouse callback
cv2.imshow("Measure Wells", image)
cv2.setMouseCallback("Measure Wells", draw_circle)

cv2.waitKey(0)
cv2.destroyAllWindows()
