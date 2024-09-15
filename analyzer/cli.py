from analyzer.image_processor import ImageProcessor
from analyzer.well_detector import WellDetector
from analyzer.well_analyzer import WellAnalyzer
from analyzer.visualizer import Visualizer
from analyzer.hsv_thresholder import HsvThresolder
from pathlib import Path


import click

@click.group()
def cli():
    pass

@cli.command()
@click.option(
    "-i",
    "--image",
    "image",
    type=click.Path(path_type=Path, dir_okay=False),
    multiple=False,
    help="The image file to open.",
)
@click.option(
    "-w",
    "--width",
    "width",
    type=click.INT,
    help="The desired width to display the image.",
)
def threshold(image, width):
    thresholder = HsvThresolder(image)
    thresholder.threshold(width)


@cli.command()
@click.option(
    "-i",
    "--image",
    "images",
    type=click.Path(path_type=Path),
    multiple=True,
    help="The image file to open.",
)
def process(images):
    def process_image(image_path):
        click.echo(f'Processing {image_path}')
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

    if images[0].is_dir():
        for image_path in images[0].iterdir():
            process_image(image_path)
    else:
        process_image(images[0])


# # Run the program
if __name__ == "__main__":
    cli()