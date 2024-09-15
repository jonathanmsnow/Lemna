from image_processor import ImageProcessor
from well_detector import WellDetector
from well_analyzer import WellAnalyzer
from visualizer import Visualizer

def main(image_path):
    # Step 1: Load and preprocess the image
    processor = ImageProcessor(image_path)
    blurred_image = processor.get_blurred_image()

    # Step 2: Detect and sort circles (wells)
    detector = WellDetector(blurred_image)
    detected_circles = detector.detect_wells()
    sorted_circles = detector.sort_circles(detected_circles)

    # Step 3: Analyze duckweed for each well
    analyzer = WellAnalyzer(processor.get_original_image())
    visualizer = Visualizer(processor.get_original_image(), sorted_circles)

    for i, (x, y, r) in enumerate(sorted_circles):
        # Analyze the duckweed in the current well
        contours, total_area = analyzer.analyze_plant_area(x, y, r)
        
        # Draw the circle and contours on the image
        visualizer.draw_contours(contours)
        visualizer.add_text(x, y, r, f"Well {i}: {total_area} px")

    # Step 4: Display the final annotated image
    visualizer.draw_circles()
    visualizer.show_image('Identified Wells', 1440)


# Run the program
if __name__ == "__main__":
    main('images/start_r1_plate1_2.jpg')