# %%
import pycrs
utm19n = pycrs.parse.from_epsg_code(6348)
utm19n_proj4 = utm19n.to_proj4()
wgs84 = pycrs.parse.from_epsg_code(4326)
wgs84_proj4 = wgs84.to_proj4()

#%%
import pyproj
fromproj = pyproj.Proj(wgs84_proj4)
toproj = pyproj.Proj(utm19n_proj4)

x, y = -76.7075, 37.2707  # Williamsburg, Virginia :)
pyproj.transform(fromproj, toproj, x, y)

# %%
