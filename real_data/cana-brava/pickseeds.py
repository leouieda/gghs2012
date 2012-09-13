import fatiando as ft
import numpy as np
import simplejson as json

log = ft.log.get()
log.info(ft.log.header())

lon, lat, height, data = np.loadtxt('gravity-anomaly-residual.dat', unpack=True)
outcropx, outcropy = np.loadtxt('outcrop.txt', unpack=True)
area = [lon.min(), lon.max(), lat.min(), lat.max()]

dens_larger = 270
dens_smaller = 390

ft.vis.figure()
ft.vis.suptitle("Pick the seeds for the larger portion")
ft.vis.axis('scaled')
ft.vis.contourf(lon, lat, data, (100, 100), 80, interp=True)
ft.vis.colorbar()
ft.vis.plot(outcropx, outcropy, '-k')
# x is north = lat
seedy, seedx = ft.ui.picker.points(area, ft.vis.gca()).T
seeds = [[x*111000, y*111000, 0, {'density':dens_larger}]
            for x, y in zip(seedx, seedy)]
ft.vis.show()

with open('seeds-larger.json', 'w') as f:
    json.dump(seeds, f)

ft.vis.figure()
ft.vis.suptitle("Pick the seeds for the smaller portion")
ft.vis.axis('scaled')
ft.vis.contourf(lon, lat, data, (100, 100), 80, interp=True)
ft.vis.colorbar()
ft.vis.plot(outcropx, outcropy, '-k')
seedy, seedx = ft.ui.picker.points(area, ft.vis.gca()).T
seeds = [[x*111000, y*111000, 0, {'density':dens_smaller}]
            for x, y in zip(seedx, seedy)]
ft.vis.show()

with open('seeds-smaller.json', 'w') as f:
    json.dump(seeds, f)
