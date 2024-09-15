import numpy as np
import cv2
class WellAnalyzer:
    def __init__(self, image):
        self.image = image

    def create_well_mask(self, x, y, r):
        mask = np.zeros(self.image.shape[:2], dtype=np.uint8)
        cv2.circle(mask, (x, y), r, 255, -1)
        return mask

    def analyze_plant_area(self, x, y, r):
        mask = self.create_well_mask(x, y, r)
        well_region = cv2.bitwise_and(self.image, self.image, mask=mask)
        hsv_well = cv2.cvtColor(well_region, cv2.COLOR_BGR2HSV)

        # Define color ranges for green and brown
        mask_yellow_green = cv2.inRange(hsv_well, (10, 39, 64), (86, 250, 250))
        mask_brown = cv2.inRange(hsv_well, (8, 60, 20), (30, 255, 200))
        combined_mask = cv2.bitwise_or(mask_yellow_green, mask_brown)

        # Find contours of the green areas
        contours, _ = cv2.findContours(combined_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        total_area = sum(cv2.contourArea(c) for c in contours)

        return contours, total_area