import math

for capacity_line in range(5, 100, 5):
    print(f"{capacity_line} ========================")
    for pixel in range(1, 101):

        if pixel > capacity_line:
            result = pixel - capacity_line
            decay = math.exp(-1*result)
            print(f"{pixel}: {decay}")