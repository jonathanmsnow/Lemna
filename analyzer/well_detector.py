import cv2
import numpy as np

class WellDetector:
    def __init__(self, blurred_image):
        self.blurred_image = blurred_image

    def detect_wells(self, dp=1, minDist=250, param1=45, param2=30, minRadius=155, maxRadius=180):
        circles = cv2.HoughCircles(self.blurred_image, cv2.HOUGH_GRADIENT, dp, minDist,
                                   param1=param1, param2=param2, minRadius=minRadius, maxRadius=maxRadius)
        return np.round(circles[0, :]).astype("int") if circles is not None else []

    def sort_circles(self, circles):
        circles_sorted = sorted(circles, key=lambda c: c[1])
        row_threshold = 40
        rows = []
        current_row = []
        previous_y = circles_sorted[0][1] if circles_sorted else 0

        for circle in circles_sorted:
            x, y, r = circle
            if abs(y - previous_y) > row_threshold:
                rows.append(sorted(current_row, key=lambda c: c[0]))
                current_row = [circle]
                previous_y = y
            else:
                current_row.append(circle)
                previous_y = y

        if current_row:
            rows.append(sorted(current_row, key=lambda c: c[0]))

        return [circle for row in rows for circle in row]
