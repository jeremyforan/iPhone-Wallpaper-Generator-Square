import random
from PIL import ImageColor


def roll_dice_on_probability(occurrence: float):
    if random.random() > (occurrence / 100):
        return True
    return False


def color_to_tuple(hex_color: str):
    if hex_color[0] != '#':
        hex_color = '#' + hex_color
    color = ImageColor.getrgb(hex_color)
    return color


class ArtDirector:
    def __init__(self, palette):
        self.palette = palette
        self.horizon = 0

    def _last_color(self):
        return self.palette[-1]

    def _first_color(self):
        return self.palette[0]

    def get_uncharged_color(self, distance_from_horizon: int):
        if roll_dice_on_probability(distance_from_horizon):
            return color_to_tuple(self._first_color())

        black = (0, 0, 0)
        return black

    def get_charged_color(self, distance_from_horizon: int):
        color_segments = len(self.palette)
        segment_size = int(100/color_segments)
        color_index = int(distance_from_horizon/segment_size) - 1
        if color_index < 1:
            color_index = 0
        color = color_to_tuple(self.palette[color_index])
        return color

    def color_me_bad(self, pixel_location):
        if pixel_location > self.horizon:
            distance_from_horizon = pixel_location - self.horizon
            color = self.get_uncharged_color(distance_from_horizon)
        else:
            distance_from_horizon = self.horizon - pixel_location
            color = self.get_charged_color(distance_from_horizon)

        return color