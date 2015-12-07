from PIL import Image
from noise import snoise2

class Map:

    def __init__(self):
        self.size = (500, 500)
        self.image = Image.new("RGBA", self.size)

    def run(self):
        pixels = self.image.load()
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                freq = 80
                octaves = 2
                px = int(snoise2(x / freq, y / freq, octaves) * 127.0 + 128.0)
                pixels[x, y] = (px, px, px)
        self.image.show()

    def save(self, f):
        self.image.save(f)

if __name__ == "__main__":
    m = Map().run()
