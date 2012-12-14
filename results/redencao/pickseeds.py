"""Pick a set of seeds on the map. Sets the right density and uses depth = 1.
Saves to seeds.json. Edit the depth accordingly
"""
import fatiando as ft
import numpy as np
import json

outcropx, outcropy = np.loadtxt('outcrop.xyz', unpack=True)
x, y, data = np.loadtxt('data.xyz', unpack=True)
z = -0.1*np.ones_like(x)

shape = (100, 100)
ft.vis.figure()
ft.vis.title("True: color | Inversion: contour")
ft.vis.axis('scaled')
levels = ft.vis.contourf(y, x, data, shape, 8, interp=True)
ft.vis.colorbar()
ft.vis.plot(outcropy, outcropx, '-k', linewidth=2)
ft.vis.xlabel('East (km)')
ft.vis.ylabel('North (km)')
ft.vis.m2km()

area = [x.min(), x.max(), y.min(), y.max()]
points = ft.ui.picker.points(area, ft.vis.gca(), xy2ne=True)
ft.vis.show()

depth = 1
prop = {"density":-90}
with open('seeds.json', 'w') as f:
    json.dump([[sx, sy, depth, prop] for sx, sy in points], f, indent=2)
