import fatiando as ft
import numpy as np
import cPickle as pickle

x, y, height, z, gxx, gxy, gxz, gyy, gyz, gzz = np.loadtxt('data.xyz').T
predicted = np.loadtxt('predicted.txt', unpack=True)[2:]

with open('seeds.pickle') as f:
    seeds = pickle.load(f)
sx, sy = np.transpose([s.center()[:2] for s in seeds])

titles = ['gyz', 'gzz']
size = (5, 5)
fmt = '.png'
dpi = 150
shape = (100, 100)
data = [gyz, gzz]
def adjust():
    #ft.vis.subplots_adjust(right=0.96, bottom=0.15)
    pass
n = 10
for i in range(2):
    # Just the data
    ft.vis.figure(figsize=size)
    adjust()
    ft.vis.title(titles[i])
    ft.vis.axis('scaled')
    levels = ft.vis.contourf(y, x, data[i], shape, n, interp=True)
    cb = ft.vis.colorbar(shrink=1)
    cb.set_label('Eotvos')
    ft.vis.xlabel('Easting (km)')
    ft.vis.ylabel('Northing (km)')
    ft.vis.m2km()
    ft.vis.savefig(titles[i] + fmt, dpi=dpi)
    # The data + seeds
    ft.vis.figure(figsize=size)
    adjust()
    ft.vis.title(titles[i])
    ft.vis.axis('scaled')
    levels = ft.vis.contourf(y, x, data[i], shape, n, interp=True)
    cb = ft.vis.colorbar(shrink=1)
    cb.set_label('Eotvos')
    ft.vis.plot(sy, sx, 'ok')
    ft.vis.xlabel('Easting (km)')
    ft.vis.ylabel('Northing (km)')
    ft.vis.m2km()
    ft.vis.savefig(titles[i] + '_seeds' + fmt, dpi=dpi)
    # The fit
    ft.vis.figure(figsize=size)
    adjust()
    ft.vis.title(titles[i])
    ft.vis.axis('scaled')
    levels = ft.vis.contourf(y, x, data[i], shape, n, interp=True)
    cb = ft.vis.colorbar(shrink=1)
    cb.set_label('Eotvos')
    ft.vis.contour(y, x, predicted[i], shape, levels, color='k', interp=True)
    ft.vis.xlabel('Easting (km)')
    ft.vis.ylabel('Northing (km)')
    ft.vis.m2km()
    ft.vis.savefig(titles[i] + '_fit' + fmt, dpi=dpi)
#ft.vis.show()

with open('result.pickle') as f:
    mesh = pickle.load(f)
bounds = mesh.bounds

ft.vis.figure3d()
ft.vis.prisms(seeds, 'density')
#ft.vis.prisms(ft.msh.ddd.vremove(0, 'density', mesh), 'density')
ft.vis.prisms(mesh, 'density')
ft.vis.axes3d(ft.vis.outline3d(bounds), fmt='%.1f', nlabels=3,
    ranges=[b*0.001 for b in bounds])
ft.vis.wall_bottom(bounds)
ft.vis.wall_north(bounds)
ft.vis.show3d()
