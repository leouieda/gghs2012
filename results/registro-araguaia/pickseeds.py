import fatiando as ft
import numpy as np
import simplejson as json

log = ft.log.get()
log.info(ft.log.header())

y, x, height, data = np.loadtxt('gravity-anomaly.dat', unpack=True,
    usecols=[2, 3, 4, 6])
# Convert from km to m
x, y = x*1000, y*1000
area = [y.min(), y.max(), x.min(), x.max()]

# Got the density from the paper Dutra, Marangoni, and Junqueira-Brod (2012)
density = 300

ft.vis.figure()
ft.vis.suptitle("Pick the seeds")
ft.vis.axis('scaled')
ft.vis.contourf(y, x, data, (200, 200), 80, interp=True)
ft.vis.colorbar()
seedy, seedx = ft.ui.picker.points(area, ft.vis.gca()).T
seeds = [[sx, sy, 2000, {'density':density}] for sx, sy in zip(seedx, seedy)]
ft.vis.show()

with open('seeds.json', 'w') as f:
    json.dump(seeds, f)
