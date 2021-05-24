import random

import square
from typing import List
import operator




class Square:
    def __init__(self, height: int, width: int, x: int, y: int):
        self.height = height
        self.width  = width

        self.x = x
        self.y = y

        self.node_x = 0
        self.node_y = 0

        self.random_node()

    def random_node(self, buffer=10) -> (int, int):
        xmin = self.x + buffer
        ymin = self.y + buffer

        xmax = self.x + self.height - buffer
        ymax = self.y + self.width - buffer

        self.node_x = random.randint(xmin, xmax)
        self.node_y = random.randint(ymin, ymax)

        return self.node_x, self.node_y

    def get_node_coordinates(self) -> (int, int):
        return self.node_x, self.node_y


class Squares:
    def __init__(self, height: int, width: int, rows: int, cols: int):
        self.collection = []
        for r in range(rows):
            tmp_row = []
            for c in range(cols):
                tmp_row.append(Square(height, width, height*c, width*r))

            self.collection.append(tmp_row)

    def return_all_nodes(self):
        nodes = []
        for x in self.collection:
            for q in x:
                nodes.append((q.node_x, q.node_y))

        return nodes

    def all_lines(self):
        row_lines = []
        col_lines = []
        all_rows = []
        for row in self.collection:
            row_lines.extend(lines_from_nodes(row))

        transposed_array = [[self.collection[j][i] for j in range(len(self.collection))] for i in range(len(self.collection[0]))]
        for row in transposed_array:
            col_lines.extend(lines_from_nodes(row))

        all_rows.extend(row_lines)
        all_rows.extend(col_lines)

        return all_rows


def lines_from_nodes(nodes: List[Square]):
    lines = []
    for node_index in range(len(nodes)-1):
        s_x, s_y = nodes[node_index].get_node_coordinates()
        e_x, e_y = nodes[node_index+1].get_node_coordinates()
        lines.append([s_x, s_y, e_x, e_y])

    return lines


class Box:
    def __init__(self, tl_square: Square, tr_square: Square, bl_square: Square, br_square: Square, color=(0,0,0,0)):
        self.tl_xy = tl_square.get_node_coordinates()
        self.tr_xy = tr_square.get_node_coordinates()
        self.bl_xy = bl_square.get_node_coordinates()
        self.br_xy = br_square.get_node_coordinates()

        self.color = color

    def set_color(self, color):
        self.color = color

    def get_box_parameter(self):
        parameter = [self.tl_xy, self.tr_xy, self.bl_xy, self.br_xy]
        return parameter

    def get_center(self):

        sum_x_1, sum_y_1 = tuple(map(operator.add, self.tl_xy, self.tr_xy))
        sum_x_2, sum_y_2 = tuple(map(operator.add, self.bl_xy, self.br_xy))

        sum_x, sum_y = tuple(map(operator.add, (sum_x_1, sum_y_1), (sum_x_2, sum_y_2)))

        return int(sum_x/4), int(sum_y/4)


def squares_to_fillable_retangles(sqr: Squares):
    boxes = []

    for r_index in range(0 ,len(sqr.collection)-1):
        for c_index in range(0, len(sqr.collection[r_index])-1):
            boxes.append(
                Box(
                    sqr.collection[r_index]     [c_index],
                    sqr.collection[r_index]     [c_index + 1],
                    sqr.collection[r_index + 1] [c_index + 1],
                    sqr.collection[r_index + 1] [c_index],
                )
            )
    return boxes
