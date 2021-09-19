#%%
import os
import pathlib

from matplotlib.pyplot import imshow
import pandas as pd
from PIL import Image
from PIL import ImageDraw

from photoheading.map import Map

data_folder = pathlib.Path(os.getcwd()).parent / 'data' 
# data_folder = pathlib.Path(__file__).parents[1] / 'data' 
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
xmin = None
ymin = None
xmax = None
ymax = None
df = pd.DataFrame()
for source in photos:
    drone_photo = Photo(source)
    coords = drone_photo.get_coordinates()
    coords = drone_photo.get_coordinates(6348)
    map.draw_circle(coords[0], coords[1])
    x = int(coords[0])
    y = int(coords[1])
    df = df.append({'File': source, 'X': x, 'Y': y}, ignore_index=True)

    raw_photo = Image.open(source)
    paper_x, paper_y = map.get_paper_coords(x, y)
    print('Pasting: {}, {}'.format(paper_x, paper_y))
    map.image.paste(raw_photo, (int(paper_x), int(paper_y)))

xmin = df['X'].min()
xmax = df['X'].max()
ymin = df['Y'].min()
ymax = df['Y'].max()

#%%
# draw = ImageDraw.Draw(map.image)
# draw.line((0, 0) + pil_base.size, fill=128)
# draw.line((0, pil_base.size[1], pil_base.size[0], 0), fill=128)
# draw.ellipse((1000, 750, 1020, 770), (255, 0, 0))
# cropped = map.image.crop((700, 250, 1500, 1000))

# imshow(cropped)

map.crop(xmin - 10, ymin - 10, xmax + 10, ymax + 10)
map.show_map()

# %%
