from turtle import *
import turtle as tur
from turtle import Screen
import random
import random
import colorsys

def random_point_x(image_size_px: int, padding: int):
    return random.randint(-600, 600)

def random_point_y(image_size_px: int, padding: int):
    return random.randint(-300, 300)

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


def tur_art(name: str):
    print("Generating art " + name)

    num_lines = random.randint(20,30)
    points = []
    rescale = 1.07
    image_size_px = int(360 * rescale)
    padding = int(30 * rescale)

    # Pick the colors.
    start_color = random_color()
    end_color = random_color()

    # Generate points to draw.
    for _ in range(num_lines):
        point = (
            random_point_x(image_size_px, padding),
            random_point_y(image_size_px, padding),
        )
        points.append(point)

    # Center image.
    # Find the bounding box.
    # min_x = min([p[0] for p in points])
    # max_x = max([p[0] for p in points])
    # min_y = min([p[1] for p in points])
    # max_y = max([p[1] for p in points])

    # Find offsets.
    # x_offset = (min_x - padding) - (image_size_px - padding - max_x)
    # y_offset = (min_y - padding) - (image_size_px - padding - max_y)

    # # Move all points by offset.
    # for i, point in enumerate(points):
    #     points[i] = (point[0] - x_offset // 2, point[1] - y_offset // 2)

    # Draw the points.
    current_thickness = 1.5 * rescale
    n_points = len(points) - 1
    for i, point in enumerate(points):
        

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
        tur.pencolor(line_color)
        tur.pensize(current_thickness)
        tur.penup()
        tur.goto(point)
        tur.pendown()
        tur.goto(next_point)
        

        # Increase the thickness.
        current_thickness *= rescale

    



if __name__ == "__main__":

    n = 1
    collection_name = "HK"
    screen = Screen()
    screen.colormode(255)
    screen.bgcolor("black")
    tur.hideturtle()
    for i in range(10):
        tur_art(collection_name)
        # tur.getscreen()
        # tur.getcanvas().postscript(file=f"{i}.gif")
        tur.clear()
    tur.exitonclick()








