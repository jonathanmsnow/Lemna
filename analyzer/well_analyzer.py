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
        # (hMin = 20 , sMin = 18, vMin = 0), (hMax = 179 , sMax = 255, vMax = 91)
        mask_yellow_green = cv2.inRange(hsv_well, (20, 18, 0), (179, 255, 91))
        # (hMin = 44 , sMin = 17, vMin = 0), (hMax = 179 , sMax = 255, vMax = 81)
        # mask_brown = cv2.inRange(hsv_well, (44, 17, 0), (179, 255, 81))
        # combined_mask = cv2.bitwise_or(mask_yellow_green, mask_brown)

        # Find contours of the green areas
        contours, _ = cv2.findContours(mask_yellow_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        filtered_contours = [cnt for cnt in contours if cv2.contourArea(cnt) >= 200]
        total_area = sum(cv2.contourArea(c) for c in filtered_contours)

        return filtered_contours, total_area
