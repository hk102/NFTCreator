from PIL import Image, ImageDraw, ImageChops, ImageFilter
import os
import random
import colorsys
import argparse
import cv2
import numpy as np
import time



def random_point(image_size_px: int, padding: int):
    return random.randint(padding, image_size_px - padding)


def random_color():

    # I want a bright, vivid color, so max V and S and only randomize HUE.
    h = random.random()
    s = 1
    v = 1
    float_rbg = colorsys.hsv_to_rgb(h, s, v)

    # Return as integer RGB.
    return (
        int(float_rbg[0] * 255),
        int(float_rbg[1] * 255),
        int(float_rbg[2] * 255),
    )


def interpolate(start_color, end_color, factor: float):
    # Find the color that is exactly factor (0.0 - 1.0) between the two colors.
    new_color_rgb = []
    for i in range(3):
        new_color_value = factor * end_color[i] + (1 - factor) * start_color[i]
        new_color_rgb.append(int(new_color_value))

    return tuple(new_color_rgb)


def generate_art(collection: str, name: str):
    print("Generating art " + name)

    # Figure out where we are going to put it.
    output_dir = os.path.join("output", collection)
    #image_path = os.path.join(output_dir, f"{name}.png")
    image_path = os.path.join(output_dir, f"{name}.gif")
    video_path = os.path.join(output_dir, f"{name}.mp4")

    # Set size parameters.
    rescale = 10
    image_size_px = 720 * rescale
    padding = 30 * rescale

    # Create the directory and base image.
    os.makedirs(output_dir, exist_ok=True)
    bg_color = (0, 0, 0)
    image = Image.new("RGB", (image_size_px, image_size_px), bg_color)
    #------------------------------------
    temp_img = Image.new("RGB", (image_size_px//rescale, image_size_px//rescale), bg_color)
    test = [temp_img]
    #-------------------------------------


    # How many lines do we want to draw?
    num_lines = 10
    points = []

    # Pick the colors.
    start_color = random_color()
    end_color = random_color()

    # Generate points to draw.
    for _ in range(num_lines):
        point = (
            random_point(image_size_px, padding),
            random_point(image_size_px, padding),
        )
        points.append(point)

    # Center image.
    # Find the bounding box.
    min_x = min([p[0] for p in points])
    max_x = max([p[0] for p in points])
    min_y = min([p[1] for p in points])
    max_y = max([p[1] for p in points])

    # Find offsets.
    x_offset = (min_x - padding) - (image_size_px - padding - max_x)
    y_offset = (min_y - padding) - (image_size_px - padding - max_y)

    # Move all points by offset.
    for i, point in enumerate(points):
        points[i] = (point[0] - x_offset // 2, point[1] - y_offset // 2)

    # Draw the points.
    current_thickness = 1 * rescale
    n_points = len(points) - 1
    for i, point in enumerate(points):

        # Create the overlay.
        overlay_image = Image.new("RGB", (image_size_px, image_size_px), (0, 0, 0))
        overlay_draw = ImageDraw.Draw(overlay_image)

        if i == n_points:
            # Connect the last point back to the first.
            next_point = points[0]
        else:
            # Otherwise connect it to the next element.
            next_point = points[i + 1]

        # Find the right color.
        factor = i / n_points
        line_color = interpolate(start_color, end_color, factor=factor)

        # Draw the line.
        overlay_draw.line([point, next_point], fill=line_color, width=current_thickness)
        
        # Increase the thickness.
        current_thickness += rescale

        # Add the overlay channel.
        image = ImageChops.add(image, overlay_image)

        test_image = image
        test_image = test_image.resize(
                (image_size_px // rescale, image_size_px // rescale), resample=Image.ANTIALIAS
        )

        test.append(test_image)

        #---------------------------------
        test_image = test_image.filter(ImageFilter.EDGE_ENHANCE_MORE)
        test.append(test_image)
        #---------------------------------

        

    # Image is done! Now resize it to be smooth.
    # image = image.resize(
    #     (image_size_px // rescale, image_size_px // rescale), resample=Image.ANTIALIAS
    # )

    # Save the image.
    #image.save(image_path)
    test = test + test[::-1]

    temp_img.save(fp=image_path, format='GIF', append_images=test,
         save_all=True, duration=250, loop=0)

    #--------Video-----------------
    video = cv2.VideoWriter(video_path, cv2.VideoWriter_fourcc(*'avc1'), fps =5,frameSize= (image_size_px // rescale, image_size_px // rescale))
    for image in test:
        video.write(cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR))

    video.release()
    #------------------------------



if __name__ == "__main__":

    n = 10
    collection_name = "HK"

    for i in range(n):
        generate_art(collection_name, f"{collection_name}_image_{i}")