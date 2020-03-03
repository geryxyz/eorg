import pdb
import sys
import os.path

import glob2

from ImageShade import *
from PIL import Image


if __name__ == '__main__':
    original_image_path = sys.argv[1]
    folder = sys.argv[2]
    tile_count = sys.argv[3]
    division = int(sys.argv[4])

    inputs = glob2.glob(os.path.join(folder, '**', '*.png.shade'))
    print(f"{len(inputs)} shades found")

    shades = []
    for file_path in inputs:
        shades.append(ImageShade.load(file_path))

    target = Image.open(original_image_path)
    tile_width = (target.size[0] / tile_count, target.size[1] / tile_count)
    for x in range(tile_count):
        for y in range(tile_count):
            cropped = target.crop((x * tile_width[0], y * tile_width[1], x * tile_width[0] + tile_width[0], y * tile_width[1] + tile_width[1]))
            tile_shade = ImageShade.from_img(cropped, None, division)
    pdb.set_trace()

