#%%
import os
import pathlib

from matplotlib.pyplot import imshow
from PIL import Image
from PIL import ImageDraw

from photoheading.map import Map

# data_folder = pathlib.Path(os.getcwd()).parent / 'data' 
data_folder = pathlib.Path(__file__).parents[1] / 'data' 
school = data_folder / 'input' / 'basemaps' / 'School01.jpg'

# %%
map = Map(school)
map.show_basemap()
print(map.bounds)
print(map.res)
print(map.get_paper_coords(356000, 4813600))
map.draw_circle(356000, 4813600)
# map.show_map()

# %%
from photoheading.photo import Photo
photo = Photo(data_folder / 'input' / 'photos01' / 'DJI_0235.JPG')
print(photo.get_coordinates())

# %%
print('CRS: {}'.format(map.crs))

#%%
# pil_base = Image.open(school).convert('RGBA')
# imshow(pil_base)

photo_folder = data_folder / 'input' / 'photos01'
photos = photo_folder.glob('*.*')
for source in photos:
    drone_photo = Photo(source)
    coords = drone_photo.get_coordinates(6348)
    print(coords)
    map.draw_circle(coords[0], coords[1])

#%%
# draw = ImageDraw.Draw(map.image)
# draw.line((0, 0) + pil_base.size, fill=128)
# draw.line((0, pil_base.size[1], pil_base.size[0], 0), fill=128)
# draw.ellipse((1000, 750, 1020, 770), (255, 0, 0))
cropped = map.image.crop((700, 250, 1500, 1000))

imshow(cropped)

# %%
