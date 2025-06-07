import numpy as np
import cv2


class WellAnalyzer:
    def __init__(self, image, hsv_lower_bound, hsv_upper_bound):
        self.image = image
        self.hsv_lower_bound = hsv_lower_bound
        self.hsv_upper_bound = hsv_upper_bound

    def create_well_mask(self, x, y, r):
        mask = np.zeros(self.image.shape[:2], dtype=np.uint8)
        cv2.circle(mask, (x, y), r, 255, -1)
        return mask

    def calculate_plant_contours(self, x, y, r):
        mask = self.create_well_mask(x, y, r)
        well_region = cv2.bitwise_and(self.image, self.image, mask=mask)
        hsv_well = cv2.cvtColor(well_region, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv_well, self.hsv_lower_bound, self.hsv_upper_bound)

        # Find contours of the green areas
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        filtered_contours = [cnt for cnt in contours if cv2.contourArea(cnt) >= 200]

        return filtered_contours
    
    def calculate_plant_area(self, contours):
        return sum(cv2.contourArea(c) for c in contours)
    
    def calculate_plant_perimeter(self, contours):
        return sum(cv2.arcLength(contour, closed=True) for contour in contours)
    
    def calculate_mean_rgb(self, image, contours):
        mask = np.zeros(image.shape[:2], dtype=np.uint8)
        cv2.drawContours(mask, contours, -1, color=255, thickness=cv2.FILLED)

        mean_bgr = cv2.mean(image, mask=mask)

        # Convert to RGB
        mean_rgb = (mean_bgr[2], mean_bgr[1], mean_bgr[0])
        return mean_rgb
