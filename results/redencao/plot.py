import sys
import fatiando as ft
import numpy as np
import cPickle as pickle

path = sys.argv[1]

outcropx, outcropy = np.loadtxt('outcrop.xyz', unpack=True)
x, y, data = np.loadtxt('data.xyz', unpack=True)
predicted = np.loadtxt('%s/predicted.txt' % (path), unpack=True, usecols=[-1])

with open('%s/seeds.pickle' % (path)) as f:
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
levels = ft.vis.contourf(y, x, data, shape, 12, interp=True)
cb = ft.vis.colorbar()
cb.set_label('mGal')
ft.vis.plot(outcropy, outcropx, '-r', linewidth=3)
ft.vis.xlabel('East (km)')
ft.vis.ylabel('North (km)')
ft.vis.m2km()
ft.vis.savefig('%s/gz ' % (path) + fmt, dpi=dpi)

ft.vis.figure(figsize=size)
ft.vis.title("Residuals")
ft.vis.hist(data - predicted, bins=8, color='grey')
ft.vis.xlabel('Residuals (mGal)')
ft.vis.ylabel('Number')
ft.vis.savefig('%s/residuals ' % (path) + fmt, dpi=dpi)

ft.vis.figure(figsize=size)
ft.vis.subplots_adjust(bottom=0.12)
ft.vis.title("Bouguer anomaly")
ft.vis.axis('scaled')
levels = ft.vis.contourf(y, x, data, shape, 12, interp=True)
cb = ft.vis.colorbar()
cb.set_label('mGal')
ft.vis.plot(outcropy, outcropx, '-r', linewidth=3)
ft.vis.plot(sy, sx, 'ok', markersize=10)
ft.vis.xlabel('East (km)')
ft.vis.ylabel('North (km)')
ft.vis.m2km()
ft.vis.savefig('%s/gz_seed ' % (path) + fmt, dpi=dpi)

ft.vis.figure(figsize=size)
ft.vis.subplots_adjust(bottom=0.12)
ft.vis.title("Bouguer anomaly")
ft.vis.axis('scaled')
levels = ft.vis.contourf(y, x, data, shape, 6, interp=True)
cb = ft.vis.colorbar()
cb.set_label('mGal')
ft.vis.contour(y, x, predicted, shape, levels, color='k', interp=True,
    linewidth=2)
ft.vis.xlabel('East (km)')
ft.vis.ylabel('North (km)')
ft.vis.m2km()
ft.vis.savefig('%s/gz_fit ' % (path) + fmt, dpi=dpi)

ft.vis.show()

with open('%s/result.pickle' % (path)) as f:
    mesh = pickle.load(f)
bounds = mesh.bounds

ft.vis.figure3d()
ft.vis.prisms(seeds, 'density')
ft.vis.prisms(ft.msh.ddd.vremove(0, 'density', mesh), 'density')
ft.vis.vtk.mlab.plot3d(outcropx, outcropy, np.zeros_like(outcropx),
    color=(1,0,0), tube_radius=300)
ft.vis.axes3d(ft.vis.outline3d(bounds), fmt='%.1f', nlabels=3,
    ranges=[b*0.001 for b in bounds])
ft.vis.wall_bottom(bounds)
ft.vis.wall_north(bounds)
ft.vis.show3d()
