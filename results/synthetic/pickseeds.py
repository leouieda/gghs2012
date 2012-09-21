import numpy as np
import fatiando as ft
import simplejson as json

x, y, z, gz, gzz = np.loadtxt('data.txt', unpack=True)

area = [0, 600000, 0, 600000]
density = 300
shape = (50, 50)

axes = ft.vis.figure().gca()
ft.vis.axis('scaled')
ft.vis.suptitle('gzz (Eotvos)')
ft.vis.contourf(y, x, gzz, shape, 20)
ft.vis.colorbar()
seedx, seedy = ft.ui.picker.points(area, axes, xy2ne=True).T
seeds = [[sx, sy, 5000, {'density':density}] for sx, sy in zip(seedx, seedy)]

with open('seeds.json', 'w') as f:
    json.dump(seeds, f)
