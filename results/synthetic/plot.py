import fatiando as ft
import cPickle as pickle
import numpy as np


log = ft.log.tofile(ft.log.get(), 'invert.log')
log.info(ft.log.header())

x, y, z, gz, gzz = np.loadtxt('data.txt', unpack=True)
predicted = np.loadtxt('predicted.txt', unpack=True, usecols=[-2, -1])
with open('seeds.pickle') as f:
    seeds = pickle.load(f)
sx, sy = np.transpose([s.center()[:2] for s in seeds])

shape = (50, 50)
titles = ['gz', 'gzz']
data = [gz, gzz]
size = (5, 4)
units = ['mGal', 'Eotvos']
fmt = '.png'
dpi = 600
for i in xrange(2):
    # Just the data
    ft.vis.figure(figsize=size)
    ft.vis.subplots_adjust(right=0.96, bottom=0.15)
    ft.vis.title(titles[i])
    ft.vis.axis('scaled')
    levels = ft.vis.contourf(y, x, data[i], shape, 30)
    cb = ft.vis.colorbar(shrink=1)
    cb.set_label(units[i])
    ft.vis.xlabel('Easting (km)')
    ft.vis.ylabel('Northing (km)')
    ft.vis.m2km()
    ft.vis.savefig(titles[i] + fmt, dpi=dpi)
    # The data + seeds
    ft.vis.figure(figsize=size)
    ft.vis.subplots_adjust(right=0.96, bottom=0.15)
    ft.vis.title(titles[i])
    ft.vis.axis('scaled')
    levels = ft.vis.contourf(y, x, data[i], shape, 30)
    cb = ft.vis.colorbar(shrink=1)
    cb.set_label(units[i])
    ft.vis.plot(sy, sx, 'ok')
    ft.vis.xlabel('Easting (km)')
    ft.vis.ylabel('Northing (km)')
    ft.vis.m2km()
    ft.vis.savefig(titles[i] + '_seeds' + fmt, dpi=dpi)
    # The fit
    ft.vis.figure(figsize=size)
    ft.vis.subplots_adjust(right=0.96, bottom=0.15)
    ft.vis.title(titles[i])
    ft.vis.axis('scaled')
    levels = ft.vis.contourf(y, x, data[i], shape, 4)
    cb = ft.vis.colorbar(shrink=1)
    cb.set_label(units[i])
    ft.vis.contour(y, x, predicted[i], shape, levels, color='k')
    ft.vis.xlabel('Easting (km)')
    ft.vis.ylabel('Northing (km)')
    ft.vis.m2km()
    ft.vis.savefig(titles[i] + '_fit' + fmt, dpi=dpi)
#ft.vis.show()

with open('model.pickle') as f:
    model = pickle.load(f)
with open('result.pickle') as f:
    mesh = pickle.load(f)

bounds = (x.min(), x.max(), y.min(), y.max(), 0, 20000)
# How much to exagerate the 3D plot
scale = (1, 1, 10)
scalebounds = [j*scale[i/2] for i, j in enumerate(bounds)]

ft.vis.figure3d()
actor = ft.vis.polyprisms(model, 'density',  cmap='gist_rainbow', opacity=0.6,
    edges=False)
actor.actor.actor.scale = scale
actor = ft.vis.prisms(seeds, 'density')
actor.actor.actor.scale = scale
actor = ft.vis.prisms(ft.msh.ddd.vremove(0, 'density', mesh), 'density')
actor.actor.actor.scale = scale
ft.vis.axes3d(ft.vis.outline3d(scalebounds), fmt='%.0f', nlabels=3,
    ranges=[b*0.001 for b in bounds])
ft.vis.wall_bottom(scalebounds)
ft.vis.wall_north(scalebounds)
ft.vis.show3d()
