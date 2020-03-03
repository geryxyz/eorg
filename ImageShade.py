import pickle

import math


class ImageShade(object):
    def __init__(self, path: str):
        self.measures = {}
        self.path = path

    def add_measure(self, key, value):
        self.measures[key] = value

    def save(self):
        with open(f'{self.path}.shade', 'wb') as output:
            pickle.dump(self, output)

    @staticmethod
    def load(file_path):
        with open(file_path, 'rb') as input_file:
            return pickle.load(input_file)

    @staticmethod
    def from_img(img, image_path, division=1):
        current = ImageShade(image_path)
        for div in range(division + 1):
            small_img = img.resize((div + 1, div + 1))
            for x in range(small_img.size[0]):
                for y in range(small_img.size[1]):
                    key = (div, x, y)
                    value = small_img.getpixel((x, y))
                    current.add_measure(key, value)

    def __sub__(self, other):
        if isinstance(other, ImageShade):
            if not self.measures:
                return math.inf
            aggregated_distance = 0
            for entry in self.measures.items():
                if entry[0] in other.measures:
                    other_entry = other.measures[entry[0]]
                    distance = sum([(d[0] - d[2]) ** 2 for d in zip(entry[1], other_entry[1])]) ** (1/2)
