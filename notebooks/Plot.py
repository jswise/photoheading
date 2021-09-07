#%%
import rasterio
# from matplotlib import pyplot
# src = rasterio.open(r"C:\GIS\PhotoHeading\TerraData\rast\2018_03554813_45_64104_sca.tif")
# pyplot.imshow(src.read(1), cmap='pink')
# pyplot.show()

# %%
from rasterio.plot import show
# show(src.read(), transform=src.transform)
# show(src)
# %%
import os
import pathlib

data_folder = pathlib.Path(os.getcwd()).parent / 'data' / 'input' / 'basemaps'
school = data_folder / 'School01.jpg'
src = rasterio.open(school)
show(src.read(), transform=src.transform)

# %%
