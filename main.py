import numpy as np
import pyny3d.geoms as pyny
import pylab
import matplotlib.cm as cm
import mpl_toolkits.mplot3d as mplot3d
import parse
from shapely import wkt

## 1. Parse WKT ##
#text = input('Enter 3D WKT : ')
text = 'TINZ(((0 0 0, 0 0 1, 0 1 1, 0 1 0, 0 0 0)), ((0 0 0, 0 1 0, 1 1 0, 1 0 0, 0 0 0)), ((0 0 0, 1 0 0, 1 0 1, 0 0 1, 0 0 0)), ((1 1 0, 1 1 1, 1 0 1, 1 0 0, 1 1 0)), ((0 1 0, 0 1 1, 1 1 1, 1 1 0, 0 1 0)), ((0 0 1, 1 0 1, 1 1 1, 0 1 1, 0 0 1)), ((1 1 0, 20 2 0, 5 2 0, 1 1 0)), ((0 0 2, 0 1 2, 1 1 2, 1 0 2, 0 0 2)), ((0 0 4, 0 1 4, 1 1 4, 1 0 4, 0 0 4)), ((0 0 10, 0 1 10, 1 1 10, 1 0 10, 0 0 10)), ((0 0 10, 12 20 10, 20 40 10,0 0 10)), ((20 40 10, 20 50 10, 60 60 10, 20 40 10)))'
replaced_text = text.replace("POLYHEDRALSURFACEZ", "MULTIPOLYGON").replace("TINZ", "MULTIPOLYGON")

wkt_text = wkt.loads(replaced_text).wkt
polygons = parse.parse('MULTIPOLYGON Z ({})', wkt_text)[0]

# slice
coords_list = polygons[2:len(polygons)-2].split(')), ((')

# Add each polygon to pallet
polygons = []
for coords in coords_list :
    poly = []
    split_coords = coords.split(', ')

    for idx, elem in enumerate(split_coords) :
        if idx == 0 :
            continue
        coord = elem.split(' ')
        coord = list(map(float, coord))
        poly.append(coord)
    polygons.append(np.array(poly))

place = pyny.Place(polygons)
colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']

for idx, polygon in enumerate(place.surface.polygons):
    print(polygon)
    if idx == 0 :
        fig = polygon.plot(color=colors[0], ret=True)
        continue
    polygon.plot(color=colors[idx%len(colors)], ax=fig)

# Needed when Windows
pylab.show()
