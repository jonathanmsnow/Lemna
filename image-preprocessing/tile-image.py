import cv2
import os

def split_image(input_dir, tile_size=512, overlap=0, output_root="tiles"):
    image_files = [f for f in os.listdir(input_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.tif', '.bmp'))]

    for image_file in image_files:
        image_path = os.path.join(input_dir, image_file)
        image = cv2.imread(image_path)

        if image is None:
            print(f"Skipping invalid image: {image_file}")
            continue

        h, w = image.shape[:2]
        stride = tile_size - overlap
        base_name = os.path.splitext(image_file)[0]
        image_output_dir = os.path.join(output_root, base_name)
        os.makedirs(image_output_dir, exist_ok=True)

        tile_id = 0
        for y in range(0, h, stride):
            for x in range(0, w, stride):
                x_end = min(x + tile_size, w)
                y_end = min(y + tile_size, h)

                tile = image[y:y_end, x:x_end]

                pad_x = tile_size - (x_end - x)
                pad_y = tile_size - (y_end - y)

                if pad_x > 0 or pad_y > 0:
                    tile = cv2.copyMakeBorder(tile, 0, pad_y, 0, pad_x, cv2.BORDER_CONSTANT, value=0)

                tile_filename = f"{tile_id:05d}.png"
                tile_path = os.path.join(image_output_dir, tile_filename)
                cv2.imwrite(tile_path, tile)

                tile_id += 1

        print(f"Processed {image_file}: {tile_id} tiles saved to {image_output_dir}")

split_image(
    input_dir="in",
    tile_size=2048,
    overlap=64,
    output_root="split_images"
)
