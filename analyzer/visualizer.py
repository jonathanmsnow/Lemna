import cv2
class Visualizer:
    def __init__(self, original_image, circles):
        self.annotated_image = original_image.copy()
        self.circles = circles

    def draw_circles(self):
        for x, y, r in self.circles:
            cv2.circle(self.annotated_image, (x, y), r, (255, 0, 255), 2)

    def draw_contours(self, contours, color=(0, 0, 255), thickness=2):
        cv2.drawContours(self.annotated_image, contours, -1, color, thickness)

    def add_text(self, x, y, r, text):
        cv2.putText(self.annotated_image, text, (x - 20, y - r - 10), cv2.FONT_HERSHEY_SIMPLEX, 
                    1.0, (255, 0, 0), 2)

    def show_image(self, window_name, width):
        resized_image = cv2.resize(self.annotated_image, (width, int(self.annotated_image.shape[0] * (width / self.annotated_image.shape[1]))))
        cv2.imshow(window_name, resized_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def save_image(self, file_name):
        cv2.imwrite(file_name, self.annotated_image)
