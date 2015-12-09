from PIL import Image
from PIL import ImageDraw
from noise import pnoise2
import math
import numpy as np
import random

GRID = ((-1, -1), (-1, 0), (-1, 1),
    (0, -1),          (0, 1),
    (1, -1), (1, 0), (1, 1))

class Terrain:

    def __init__(self, name, threshold, color):
        self.name = name
        self.threshold = threshold
        self.color = color
 
TERRAINS = (
    Terrain("Water", 0.2, (0, 0, 255)),
    Terrain("Beach", 0.25, (0.8, 0.8, 0.2)),
    Terrain("Grass", 0.3, (0.2, 0.8, 0.2)),
    Terrain("Forest", 0.45, (0.2, 0.6, 0.2)),
    Terrain("Mountain", 0.57, (0.8, 0.8, 0.84)),
    Terrain("Snow", 1, (255, 255, 255)),
    )

def array2d(w, h):
    return np.array([[0] * w] * h, np.float32)

class Map:

    def __init__(self):
        self.size = (500, 500)
        self.image = Image.new("RGBA", self.size)
        self.heights = np.zeros(self.size, np.float32)
        self.pixels = self.image.load()
        self.tips = []

    def itergrid(self, pos):
        for c in GRID:
            cx = c[0] + pos[0]
            cy = c[1] + pos[1]
            if cx >= 0 and cx < self.size[0] and cy >= 0 and cy < self.size[1]:
                yield (cx, cy)

    def terrain(self):
        pixels = self.pixels
        center = (self.size[0]/2, self.size[1]/2)
        def dist(c):
            dx = center[0] - c[0]
            dy = center[1] - c[1]
            mag = math.sqrt(dx * dx + dy * dy)
            return mag
        ox = random.random() * 1
        oy = random.random() * 1
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                freq = 90.5
                octaves = 6
                perlin = pnoise2(ox + x / freq, oy + y / freq, octaves) + 0.5
                mag = dist((x, y)) / 300.0
                height = perlin * (1 - mag) * 1.0
                self.heights[x, y] = height
                if height < 0:
                    height = 0
                for t in TERRAINS:
                    if height < t.threshold:
                        rgb = t.color
                        if t.name == "Snow":
                            self.tips.append((x, y))
                        break
                pixels[x, y] = tuple([int(c * 255.0) for c in rgb])
        return self

    def river(self):
        x, y = random.choice(self.tips)
        WATER = (255, 0, 0)
        opens = []
        opens.append((x, y))
        closeds = set()
        while opens:
            o = sorted(opens, key=lambda x: self.heights[x])[0]
            opens.remove(o)
            closeds.add(o)
            for cd in self.itergrid(o):
                if self.heights[cd] <= 0.2:
                    return 
                elif cd not in closeds:
                    opens.append(cd)

            d = None
            h = 2
            for cd in self.itergrid(o):
                ch = self.heights[o]
                if ch < h:
                    h = ch
                    d = cd
            if d:
                self.pixels[o] = WATER
                opens = []
                opens.append(d)
            else:
                self.pixels[o] = (255, 255, 0)
                for cd in self.itergrid(o):
                    if cd not in closeds:
                        opens.append(cd)
        return self

    def feature(self):
        return
        for i in range(50):
            x = random.random() * self.size[0]
            y = random.random() * self.size[1]
            p = self.terrains[x, y]

    def directions(self):
        pass

    def save(self, f):
        self.image.save(f)
        return self

if __name__ == "__main__":
    m = Map()
    m.terrain()
    m.river()
    m.directions()
    m.save('out.png')
