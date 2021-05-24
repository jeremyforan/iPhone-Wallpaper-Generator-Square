from PIL import Image, ImageDraw, ImageColor
import random
import square
import math

palette = ["6f2dbd", "a663cc", "b298dc", "b8d0eb", "b9faf8"]

designs = {
    45: {
        0	: [100,	50,	1],
        5	: [100,	50,	1],
        10	: [100,	50,	1],
        15	: [100,	50,	1],
        20	: [100,	50,	1],
        25	: [100,	50,	2],
        30	: [100,	50,	2],
        35	: [100,	50,	2],
        40	: [100,	75,	2],
        45	: [100,	75,	3],
        50	: [75,	10,	3],
        55	: [50,	10,	3],
        60	: [25,	10,	3],
        65	: [15,	20,	4],
        70	: [5,	25,	4],
        75	: [2,	25,	5],
        80	: [2,	25,	5],
        85	: [2,	25,	5],
        90	: [2,	25,	5],
        95	: [2,	25,	5],
        100	: [2,	25,	5],
    }
}



bleed_point = (1792, 420)

raw_height  = 1800
raw_width   = 840
buffer      = 200

canvas_h = raw_height   + buffer
canvas_w = raw_width    + buffer

square_size = 80


white = (255, 255, 255, 255)

# 1792-by-828-pixel resolution at 326 ppi
crop_box = [int(buffer/2), int(buffer/2), 828 + int(buffer/2), 1792 + int(buffer/2)]


def linear_distance_percentage(xy: (int, int), location="bottom", h=1800, w=840):
    x, y = xy
    if location == "bottom":
        q_percent = int((y / h) * 100)
        return q_percent


def black_transparent():
    return 0, 0, 0, random.randint(10, 255)


def white_transparent():
    return 255, 255, 255, random.randint(10, 255)


# def color_me_bad(passed_color, occurance, varriance=10):
#     return_color = (*passed_color, random.randint(10, 255))
#     return return_color

def nearest_five(x, base=5):
    return base * round(x/base)


if __name__ == '__main__':

    sqr = square.Squares(square_size, square_size, int(canvas_h / square_size), int(canvas_w / square_size))

    all_nodes = sqr.return_all_nodes()

    all_lines = sqr.all_lines()

    lines = sqr.all_lines()

    boxes = square.squares_to_fillable_retangles(sqr)

    for design in designs.items():
        percent, schema = design

        canvas = Image.new('RGBA', (canvas_w, canvas_h), color=0)

        draw = ImageDraw.Draw(canvas)

        for box in boxes:
            box_xy = box.get_center()
            distance_percent = 100 - linear_distance_percentage(box_xy)

            if distance_percent < 0:
                distance_percent = 0

            occurrence, variance, color_index = schema[nearest_five(distance_percent)]

            if random.random() > (occurrence/100):
                color = white_transparent()
            else:

                color = ImageColor.getrgb(f"#{palette[color_index-1]}")
                if variance == 0:
                    color = (*color, 255)
                else:
                    alpha = random.randint(255-(variance*2), 255)
                    color = (*color, alpha)

            draw.polygon(box.get_box_parameter(), fill=color )

        for line in all_lines:
            draw.line(line, fill=white, width=1)

        cropped_image = canvas.crop(crop_box)

        cropped_image.save(f"output/{percent}.png", "PNG")

