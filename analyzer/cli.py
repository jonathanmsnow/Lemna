from analyzer.image_processor import ImageProcessor
from analyzer.well_detector import WellDetector
from analyzer.well_analyzer import WellAnalyzer
from analyzer.visualizer import Visualizer
from analyzer.hsv_thresholder import HsvThresolder
from pathlib import Path
import os
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
    multiple=False,
    help="The image file to open.",
)
@click.option(
    "-o",
    "--output",
    "output",
    type=click.Path(path_type=Path, dir_okay=True),
    multiple=False,
    help="The name of the directory to output to.",
)
def process(images, output):
    def process_image(image_path, output):

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

        csv_out = []
        csv_out.append("Well,area")
        for i, (x, y, r) in enumerate(sorted_circles):
            # Analyze the duckweed in the current well
            contours, total_area = analyzer.analyze_plant_area(x, y, r)

            # Draw the circle and contours on the image
            visualizer.draw_contours(contours)
            visualizer.add_text(x, y, r, f"Well {i}: {total_area} px")

            # add well number and area to output
            csv_out.append(f"{i},{total_area}")

        # Step 4: Display the final annotated image
        visualizer.draw_circles()
        #visualizer.show_image('Identified Wells', 1440)

        os.makedirs(output, exist_ok=True)
        out_name = os.path.splitext(os.path.basename(image_path))[0]
        out_file = str(output) + "/" + out_name + ".csv"
        with open(out_file, 'w') as f:
            for line in csv_out:
                f.write(line + '\n')

        out_image = str(output) + "/" + out_name + "_annotated.png"
        visualizer.save_image(out_image)


    if images.is_dir():
        for image_path in images.iterdir():
            process_image(image_path, output)
    else:
        process_image(images, output)


# # Run the program
if __name__ == "__main__":
    cli()
