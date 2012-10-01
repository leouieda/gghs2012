import sys
import os
import fatiando as ft
import numpy as np
import cPickle as pickle

path = sys.argv[1]

y, x, data = np.loadtxt('gravity-anomaly.dat', unpack=True,
    usecols=[2, 3, 6])
y, x = y*1000, x*1000
predicted = np.loadtxt(os.path.join(path, 'predicted.txt'), unpack=True,
    usecols=[-1])

with open(os.path.join(path, 'seeds.pickle')) as f:
    seeds = pickle.load(f)
sx, sy = np.transpose([s.center()[:2] for s in seeds])

fmt = '.png'
dpi = 200
size = (5.6, 4)
shape = (200, 200)

ft.vis.figure(figsize=size)
ft.vis.subplots_adjust(bottom=0.12)
ft.vis.title("Bouguer anomaly")
ft.vis.axis('scaled')
levels = ft.vis.contourf(y, x, data, shape, 20, interp=True)
cb = ft.vis.colorbar(shrink=0.86)
cb.set_label('mGal')
ft.vis.plot(y, x, 'xk')
ft.vis.xlabel('East (km)')
ft.vis.ylabel('North (km)')
ft.vis.m2km()
ft.vis.savefig('gz' + fmt, dpi=dpi)

ft.vis.figure(figsize=size)
ft.vis.subplots_adjust(bottom=0.12)
ft.vis.title("Bouguer anomaly")
ft.vis.axis('scaled')
levels = ft.vis.contourf(y, x, data, shape, 20, interp=True)
cb = ft.vis.colorbar(shrink=0.86)
cb.set_label('mGal')
ft.vis.plot(sy, sx, 'ok', markersize=8)
ft.vis.xlabel('East (km)')
ft.vis.ylabel('North (km)')
ft.vis.m2km()
ft.vis.savefig('gz_seed' + fmt, dpi=dpi)

ft.vis.figure(figsize=size)
ft.vis.subplots_adjust(bottom=0.12)
ft.vis.title("Bouguer anomaly")
ft.vis.axis('scaled')
levels = ft.vis.contourf(y, x, data, shape, 12, interp=True)
cb = ft.vis.colorbar(shrink=0.86)
cb.set_label('mGal')
ft.vis.contour(y, x, predicted, shape, levels, color='k', interp=True,
    linewidth=1.5)
ft.vis.plot(y, x, 'xk')
ft.vis.xlabel('East (km)')
ft.vis.ylabel('North (km)')
ft.vis.m2km()
ft.vis.savefig('gz_fit' + fmt, dpi=dpi)

ft.vis.show()


with open(os.path.join(path, 'result.pickle')) as f:
    mesh = pickle.load(f)
bounds = mesh.bounds

ft.vis.figure3d()
ft.vis.prisms(seeds, 'density')
ft.vis.prisms(ft.msh.ddd.vremove(0, 'density', mesh), 'density')
#ft.vis.prisms(mesh, 'density')
ft.vis.axes3d(ft.vis.outline3d(bounds), fmt='%.1f', nlabels=3,
    ranges=[b*0.001 for b in bounds])
ft.vis.wall_bottom(bounds)
ft.vis.wall_north(bounds)
ft.vis.show3d()
