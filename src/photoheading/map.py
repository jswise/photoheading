"""Define the Map class."""

from PIL import Image
from PIL import ImageDraw
from matplotlib.pyplot import imshow
import rasterio
from rasterio.plot import show

from keenepyt.core.thing import Thing

class Map(Thing):
    """Represents a map that uses a georeferenced image as a basemap."""

    def __init__(self, source, helpers=None, **kwargs) -> None:
        super().__init__(helpers, **kwargs)

        self.source = source

        with rasterio.open(source) as dataset:
            self.bounds = dataset.bounds
            self.crs = dataset.crs
            self.res = dataset.res
        
        self.image = Image.open(source).convert('RGBA')

    def crop(self, xmin, ymin, xmax, ymax):
        left, top = self.get_paper_coords(xmin, ymax)
        right, bottom = self.get_paper_coords(xmax, ymin)
        self.image = self.image.crop((left, top, right, bottom))
        self.bounds = (xmin, ymin, xmax, ymax)

    def draw_circle(self, x, y, r=2, fill='red', outline='black'):
        draw = ImageDraw.Draw(self.image)
        x_paper, y_paper = self.get_paper_coords(x, y)
        xy = (x_paper - r, y_paper - r, x_paper + r, y_paper + r)
        draw.ellipse(xy, fill, outline)
        # draw.ellipse((1000, 750, 1020, 770), fill, outline)

    def get_paper_coords(self, x, y):
        x_out = (x - self.bounds[0]) / self.res[0]
        y_out = (self.bounds[3] - y) / self.res[1]
        return x_out, y_out

    def reres(self, factor):
        """Increase the resolution of the image by the specified factor.
        
        :param factor: An integer by which to multiply the number of pixels.
        """

        new_width = self.image.width * factor
        new_height = self.image.height * factor
        self.res = (self.res[0] / factor, self.res[1] / factor)

        self.image = self.image.resize((new_width, new_height))

    def show_map(self):
        imshow(self.image)

    def show_basemap(self):
        with rasterio.open(self.source) as dataset:
            show(dataset.read(), transform=dataset.transform)
    
    def write(self, path):
        rgb = self.image.convert('RGB')
        rgb.save(path)
