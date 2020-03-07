import pdb
import random
import sys
import os.path

import glob2

from ImageShade import *
from PIL import Image


if __name__ == '__main__':
    original_image_path = sys.argv[1]
    folder = sys.argv[2]
    tile_count = int(sys.argv[3])
    division = int(sys.argv[4])

    distances_allowance = .1

    inputs = glob2.glob(os.path.join(folder, '**', '*.png.shade'))
    print(f"{len(inputs)} shades found")

    print("loading shades... ", end='')
    sys.stdout.flush()
    shades = []
    for file_path in inputs:
        shades.append(ImageShade.load(file_path))
    print("done")

    target = Image.open(original_image_path)
    temp_image = Image.open(shades[0].path)
    mont_width = (int(temp_image.size[0] * .1), int(temp_image.size[1] * .1))
    print(f"monts will be {mont_width[0]}X{mont_width[1]}")
    montage = Image.new('RGBA', (mont_width[0] * tile_count, mont_width[1] * tile_count))
    print(f"montage will be {montage.size[0]}X{montage.size[1]}")
    tile_width = (target.size[0] / tile_count, target.size[1] / tile_count)
    for x in range(tile_count):
        print(f"{x}: ", end='')
        sys.stdout.flush()
        for y in range(tile_count):
            cropped = target.crop((x * tile_width[0], y * tile_width[1], x * tile_width[0] + tile_width[0], y * tile_width[1] + tile_width[1]))
            tile_shade = ImageShade.from_img(cropped, None, division)
            distances = {}
            for shade in shades:
                distances[shade] = tile_shade - shade
            max_distance = max(distances.values())
            sorted_distances = sorted(distances.items(), key=lambda e: e[1])
            candidates = [e for e in sorted_distances if abs(e[1] - sorted_distances[0][1]) < max_distance * distances_allowance]
            selection = sorted_distances[0]
            if candidates:
                selection = random.choice(candidates)
                print(":", end='')
            else:
                print("!", end='')
            montage.paste(Image.open(selection[0].path).resize(mont_width), (x * mont_width[0], y * mont_width[1]))
            sys.stdout.flush()
        print()
    montage.save("out.png")
