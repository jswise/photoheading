#%%
import math
import pathlib

from matplotlib.pyplot import imshow
import numpy as np
import pandas as pd
from PIL import Image
from PIL import ImageDraw

from photoheading.map import Map

# data_folder = pathlib.Path(os.getcwd()).parent / 'data' 
data_folder = pathlib.Path(__file__).parents[1] / 'data' 
school = data_folder / 'input' / 'basemaps' / 'School01.jpg'
print(data_folder)

# %%
map = Map(school)
map.reres(4)
# map.show_basemap()
print(map.bounds)
print(map.res)
# print(map.get_paper_coords(356000, 4813600))
# map.draw_circle(356000, 4813600)
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

def get_alpha(im_w, im_h):

    third_w = int(im_w / 3)
    third_h = int(im_h / 3)

    left_grad = np.linspace(0, 255, third_w)
    middle_length = im_w - (third_w * 2)
    middle_section = np.full(middle_length, 255)
    right_grad = np.flip(left_grad)
    horiz_vec = np.append(np.append(left_grad, middle_section), right_grad)
    horiz_mat = np.tile(horiz_vec, (im_h, 1))

    top_grad = np.linspace(0, 255, third_h)
    middle_length = im_h - (third_h * 2)
    middle_section = np.full(middle_length, 255)
    bottom_grad = np.flip(top_grad)
    vert_vec = np.append(np.append(top_grad, middle_section), bottom_grad)
    vert_mat = np.tile(vert_vec, (im_w, 1)).T

    combined_mat = np.minimum(horiz_mat, vert_mat)

    return Image.fromarray(np.uint8(combined_mat))

def get_course(x, y, prev_x, prev_y):
    if prev_x is None:
        return 0
    dx = x - prev_x
    dy = y - prev_y
    if dx == 0:
        if dy >= 0:
            return 0
        elif dy < 0:
            return 180
    atan_rad = math.atan(dy / dx)
    atan_deg = atan_rad * 180 / math.pi
    if dx > 0:
        return int(90 - atan_deg)
    else:
        return int(270 - atan_deg)

def build_photo_table(photo_folder):
    spacing = 3
    photos = list(photo_folder.glob('*.*'))
    photo_count = int(len(photos) / spacing)
    df = pd.DataFrame()
    prev_x = None
    prev_y = None
    i = 0
    for photo_file in photos:
        i += 1
        if i % spacing > 0:
            continue
        percent = int((i / photo_count) * 100)
        print('Processing {} of {} ({}%).'.format(i, photo_count, percent))
        drone_photo = Photo(photo_file)
        # coords = drone_photo.get_coordinates()
        coords = drone_photo.get_coordinates(6348)
        x = int(coords[0])
        y = int(coords[1])
        row = {
            'File': photo_file,
            'X': x,
            'Y': y,
            'PrevX': prev_x,
            'PrevY': prev_y
        }
        row['Course'] = get_course(x, y, prev_x, prev_y)
        df = df.append(row, ignore_index=True)
        prev_x = x
        prev_y = y
    if photo_count > 1:
        df['Course'][0] = df['Course'][1]
    mean_courses = [df['Course'][0]]
    for i in range(1, photo_count - 1):
        course = df['Course'][i]
        next_course = course = df['Course'][i + 1]
        if abs(next_course - course) > 10:
            mean_courses.append(-1)
        else:
            mean_courses.append((course + next_course) / 2)
    mean_courses.append(df['Course'][photo_count - 1])
    df['MeanCourse'] = mean_courses
    return df

photo_path = data_folder / 'input' / 'photos01' / 'DJI_0235.JPG'
test_photo = Image.open(photo_path)
im_w, im_h = test_photo.size
alpha = get_alpha(im_w, im_h)
test_photo.putalpha(alpha)
white = Image.new('RGBA', test_photo.size, color=0xFFFFFF)
white.paste(test_photo, (0, 0), test_photo)
rgb = white.convert('RGB')
rgb.save(data_folder / 'output' / 'TestPhoto.jpg')

# photo_folder = data_folder / 'input' / 'photos01'
# photo_folder = pathlib.Path(r'C:\Personal\YCEMA\20210522\Subset01')
photo_folder = pathlib.Path(r'C:\Personal\YCEMA\20210522\Yellow01')
photo_table = build_photo_table(photo_folder)
northeast = (photo_table['Course'] > 25) & (photo_table['Course'] < 50)
photo_table.loc[northeast, 'MeanCourse'] = photo_table[northeast]['Course'].mean()
southwest = (photo_table['Course'] > 110) & (photo_table['Course'] < 230)
# photo_table.loc[southwest, 'MeanCourse'] = photo_table[southwest]['Course'].mean()
photo_table.loc[southwest, 'MeanCourse'] = -1
print(photo_table[['X', 'Y', 'PrevX', 'PrevY', 'Course', 'MeanCourse']])
crab = 6
# crab = 0
photo_count = len(photo_table)
i = 0
paper_coords = []
for _, row in photo_table.iterrows():
    i += 1
    # if i < 10:
    #     continue
    percent = int((i / photo_count) * 100)
    raw_photo = Image.open(row['File'])
    new_width = int(raw_photo.width / 8)
    new_height = int(raw_photo.height / 8)
    # raw_photo = apply_gradient(raw_photo)
    raw_photo.putalpha(alpha)
    small_photo = raw_photo.resize((new_width, new_height))
    small_photo = small_photo.convert('RGBA')
    # small_photo = small_photo.rotate(132, expand=True, fillcolor=(0, 0, 255, 0))
    course = row['MeanCourse']
    if course == -1:
        continue
    theta = crab - course
    print('Pasting {} of {} ({}%).'.format(i, photo_count, percent))
    small_photo = small_photo.rotate(theta, expand=True, fillcolor=(0, 0, 255, 0))
    center_x, center_y = map.get_paper_coords(row['X'], row['Y'])
    paper_coords.append([center_x, center_y])
    corner_x = center_x - int(small_photo.width / 2)
    corner_y = center_y - int(small_photo.height / 2)

    
    # print('Pasting: {}, {}'.format(paper_x, paper_y))
    map.image.paste(small_photo, (int(corner_x), int(corner_y)), small_photo)
    # map.image.alpha_composite(small_photo)

# prev_x = None
# prev_y = None
# for _, row in photo_table.iterrows():
#     if prev_x:
#         map.draw_line(prev_x, prev_y, row['X'], row['Y'], width=4)
#     prev_x = row['X']
#     prev_y = row['Y']
# for _, row in photo_table.iterrows():
#     map.draw_circle(row['X'], row['Y'], 6, 'yellow')

xmin = photo_table['X'].min()
xmax = photo_table['X'].max()
ymin = photo_table['Y'].min()
ymax = photo_table['Y'].max()

# draw = ImageDraw.Draw(map.image)
# draw.line((0, 0) + pil_base.size, fill=128)
# draw.line((0, pil_base.size[1], pil_base.size[0], 0), fill=128)
# draw.ellipse((1000, 750, 1020, 770), (255, 0, 0))
# cropped = map.image.crop((700, 250, 1500, 1000))

# imshow(cropped)

map.crop(xmin - 50, ymin - 50, xmax + 50, ymax + 50)
map.show_map()
map.write(data_folder / 'output' / 'Map.jpg')
print('Done.')