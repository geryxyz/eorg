import os.path
import sys

import glob2
from PIL import Image

from ImageShade import *

if __name__ == '__main__':
    folder = sys.argv[1]
    division = int(sys.argv[2])

    inputs = glob2.glob(os.path.join(folder, '**', '*.png'))
    print(f"{len(inputs)} image found")

    for image_path in inputs:
        print(f"scanning {image_path} image")
        img = Image.open(image_path)
        ImageShade.from_img(img, image_path, division).save()

