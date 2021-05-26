from PIL import Image, ImageDraw, ImageColor
import random
import square
import artDirector
import math

# palette = ["6f2dbd", "a663cc", "b298dc", "b8d0eb", "b9faf8"]

palette = ['#ff00ff', '#fd02ff', '#fa05ff', '#f807ff', '#f50aff',
           '#f30cff', '#f00fff', '#ee11ff', '#eb14ff', '#e817ff',
           '#e619ff', '#e31cff', '#e11eff', '#de21ff', '#dc23ff',
           '#d926ff', '#d728ff', '#d42bff', '#d12eff', '#cf30ff',
           '#cc33ff', '#ca35ff', '#c738ff', '#c53aff', '#c23dff',
           '#bf40ff', '#bd42ff', '#ba45ff', '#b847ff', '#b54aff',
           '#b34cff', '#b04fff', '#ae51ff', '#ab54ff', '#a857ff',
           '#a659ff', '#a35cff', '#a15eff', '#9e61ff', '#9c63ff',
           '#9966ff', '#9768ff', '#946bff', '#916eff', '#8f70ff',
           '#8c73ff', '#8a75ff', '#8778ff', '#857aff', '#827dff',
           '#7f80ff', '#7d82ff', '#7a85ff', '#7887ff', '#758aff',
           '#738cff', '#708fff', '#6e91ff', '#6b94ff', '#6897ff',
           '#6699ff', '#639cff', '#619eff', '#5ea1ff', '#5ca3ff',
           '#59a6ff', '#57a8ff', '#54abff', '#51aeff', '#4fb0ff',
           '#4cb3ff', '#4ab5ff', '#47b8ff', '#45baff', '#42bdff',
           '#3fc0ff', '#3dc2ff', '#3ac5ff', '#38c7ff', '#35caff',
           '#33ccff', '#30cfff', '#2ed1ff', '#2bd4ff', '#28d7ff',
           '#26d9ff', '#23dcff', '#21deff', '#1ee1ff', '#1ce3ff',
           '#19e6ff', '#17e8ff', '#14ebff', '#11eeff', '#0ff0ff',
           '#0cf3ff', '#0af5ff', '#07f8ff', '#05faff', '#02fdff']

bleed_point = (1792, 420)

raw_height  = 1800
raw_width   = 840
buffer      = 200

canvas_h = raw_height   + buffer
canvas_w = raw_width    + buffer

square_size = 30

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


def nearest_five(x, base=5):
    return base * round(x/base)


if __name__ == '__main__':

    ad = artDirector.ArtDirector(palette)

    sqr = square.Squares(square_size, square_size, int(canvas_h / square_size), int(canvas_w / square_size))

    all_nodes = sqr.return_all_nodes()

    all_lines = sqr.all_lines()

    lines = sqr.all_lines()

    boxes = square.squares_to_fillable_retangles(sqr)

    for percent in range(0, 100, 5):
        ad.horizon = percent

        canvas = Image.new('RGBA', (canvas_w, canvas_h), color=0)

        draw = ImageDraw.Draw(canvas)

        for box in boxes:
            box_xy = box.get_center()
            distance_percent = 100 - linear_distance_percentage(box_xy)

            if distance_percent < 0:
                distance_percent = 0

            color = ad.color_me_bad(distance_percent)

            color = (*color, 255)

            draw.polygon(box.get_box_parameter(), fill=color)

        for line in all_lines:
            draw.line(line, fill=white, width=1)

        cropped_image = canvas.crop(crop_box)

        cropped_image.save(f"output/{percent}.png", "PNG")


    # charing port
    canvas = Image.new('RGBA', (canvas_w, canvas_h), color=0)

    draw = ImageDraw.Draw(canvas)

    for box in boxes:
        box_xy = box.get_center()

        draw.polygon(box.get_box_parameter(), fill=(0,0,0))

    for line in all_lines:
        draw.line(line, fill=(255,204,0), width=1)

    cropped_image = canvas.crop(crop_box)

    cropped_image.save(f"output/charging.png", "PNG")

