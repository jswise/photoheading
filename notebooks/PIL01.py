#%%
import pathlib

from matplotlib.pyplot import imshow
import numpy as np
from PIL import Image, ImageDraw

raw_folder = r'C:\GIS\Novi\xData\20_09_25_NOVI_Raw_Images'
rast_folder = r'C:\GIS\Novi\TerraData\Rast'

basemap_scale = 1.28

# %%
# Adapted from https://stackoverflow.com/questions/39976028/python-pillow-make-gradient-for-transparency
def apply_gradient(im):
    # if im.mode != 'RGBA':
    #     im = im.convert('RGBA')
    # width, height = im.size
    # gradient = Image.new('L', (1, 255), color=0xFF)
    # for i in range(255):
    #     gradient.putpixel((0, i), i)
    im_h = im.size[1]
    gradient = Image.new('L', (1, im_h), color=0xFF)
    start_y = 500
    for i in range(im_h):
        gradient.putpixel((0, i), i - start_y)
    alpha = gradient.resize(im.size)
    # black_im = Image.new('RGBA', (width, height), color=0) # i.e. black
    # print('{}, {}'.format(black_im.mode, alpha.mode))
    im.putalpha(alpha)
    # print('{}, {}'.format(im.mode, black_im.mode))
    # gradient_im = Image.alpha_composite(im, black_im)
    # return gradient_im
    return im

# Pasted from https://stackoverflow.com/questions/53032270/perspective-transform-with-python-pil-using-src-target-coordinates

def find_coeffs(source_coords, target_coords):
    matrix = []
    for s, t in zip(source_coords, target_coords):
        matrix.append([t[0], t[1], 1, 0, 0, 0, -s[0]*t[0], -s[0]*t[1]])
        matrix.append([0, 0, 0, t[0], t[1], 1, -s[1]*t[0], -s[1]*t[1]])
    A = np.matrix(matrix, dtype=float)
    B = np.array(source_coords).reshape(8)
    res = np.dot(np.linalg.inv(A.T * A) * A.T, B)
    return np.array(res).reshape(8)

def squash(raw_photo, bottom_frac):
    w, h = raw_photo.size
    input_extent = [(0, 0), (w, 0), (w, h), (0, h)]
    offset = w * (1 - bottom_frac) / 2
    output_extent = [(0, 0), (w, 0), (w - offset, h), (offset, h)]
    coeffs = find_coeffs(input_extent, output_extent)

    return raw_photo.transform(raw_photo.size, Image.PERSPECTIVE, coeffs,
              Image.BICUBIC)

# %%
rast_path = pathlib.Path(rast_folder)
basemap_path = rast_path.joinpath('Basemap.jpg')
raw_base = Image.open(basemap_path).convert('RGBA')
w_raw, h_raw = raw_base.size
w = int(w_raw * basemap_scale)
h = int(h_raw * basemap_scale)

# %%
raw_folder_path = pathlib.Path(raw_folder)
gen = raw_folder_path.glob('*.jpg')
photos = [x for x in gen if x.is_file()]

# %%
basemap = raw_base.resize((w, h))
crop_rect = (100, 0, 1000, 1250)

translations = [
    [-1.62, 0.3, 174.2],
    [-1.597, 0.24, 174.2],
    [-1.597, 0.23, 174.2],
    [-1.597, 0.25, 174.2],
    [-1.597, 0.25, 174.2],
    [-1.597, 0.25, 174.2],
    [-1.597, 0.25, 174.2],
    [-1.725, 0.23, 170],
    [-1.597, 0.25, 174.2],
    [-1.597, 0.25, 174.2],
    [-1.597, 0.25, 174.2],
    [-1.597, 0.25, 174.2],
    [-1.597, 0.25, 174.2],
    [-1.597, 0.25, 174.2],
    [-1.7475, 0.215, 169],
    [-1.597, 0.25, 174.2],
    [-1.597, 0.25, 174.2],
    [-1.597, 0.25, 174.2],
    [-1.597, 0.25, 174.2],
    [-1.597, 0.25, 174.2],
    [-1.597, 0.25, 174.2],
    [-1.597, 0.25, 174.2],
    [-1.697, 0.18, 170.4],
    [-1.597, 0.25, 174.2],
    [-1.597, 0.25, 174.2],
    [-1.597, 0.25, 174.2],
    [-1.69, 0.13, 170],
    [-1.597, 0.25, 174.2],
    [-1.597, 0.25, 174.2],
    [-1.677, 0.09, 170],
]

def add_photo(file_path, x_frac, y_frac, theta, scale=1.0):
    raw_photo = Image.open(file_path)
    gradient_im = apply_gradient(raw_photo)
    # gradient_im = raw_photo
    squashed = squash(gradient_im, 0.032)
    trans_canvas = Image.new('RGBA', basemap.size, 0xFF)
    squash01 = squashed.rotate(theta)
    x = int(x_frac * w)
    y = int(y_frac * h)
    trans_canvas.paste(squash01, (x, y))#, mask=squash01)
    # squash02 = squashed.rotate(55)
    # trans_canvas.paste(squash02, (50, 50), squash02)
    basemap.alpha_composite(trans_canvas)
    imshow(np.asarray(basemap.crop(crop_rect)))
    # imshow(np.asarray(basemap))

    # imshow(np.asarray(raw_photo))

# for i, photo in enumerate(photos):
for i in [
    0,
    7,
    14,
    22,
    26,
    29
]:
# for i in [14]:
    photo = photos[i]
    translation = translations[i]
    add_photo(photo, translation[0], translation[1], translation[2])

def add_drawing(file_path, x_frac, y_frac, theta, scale=1.0):
    raw_photo = Image.open(file_path)
    print(raw_photo.mode)
    raw_photo = raw_photo.convert('RGBA')
    # gradient_im = apply_gradient(raw_photo)
    gradient_im = raw_photo
    squashed = squash(gradient_im, 0.032)
    trans_canvas = Image.new('RGBA', basemap.size, 0xFF)
    squash01 = squashed.rotate(theta)
    x = int(x_frac * w)
    y = int(y_frac * h)
    trans_canvas.paste(squash01, (x, y))#, mask=squash01)
    # squash02 = squashed.rotate(55)
    # trans_canvas.paste(squash02, (50, 50), squash02)
    basemap.alpha_composite(trans_canvas)
    imshow(np.asarray(basemap.crop(crop_rect)))
    # imshow(np.asarray(basemap))

    # imshow(np.asarray(raw_photo))

drawing = r"C:\GIS\Novi\TerraData\Rast\Drawing99.png"
translation = translations[29]
add_drawing(drawing, translation[0], translation[1], translation[2])

drawing = r"C:\GIS\Novi\TerraData\Rast\Drawing96.png"
translation = translations[26]
add_drawing(drawing, translation[0], translation[1], translation[2])

drawing = r"C:\GIS\Novi\TerraData\Rast\Drawing92.png"
translation = translations[22]
add_drawing(drawing, translation[0], translation[1], translation[2])

basemap.convert('RGB').crop(crop_rect).save(rast_path.joinpath('Pasted.jpg'))



# %%
