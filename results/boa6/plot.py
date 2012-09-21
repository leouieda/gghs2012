import fatiando as ft
import numpy as np
import cPickle as pickle

x, y, height, z, gxx, gxy, gxz, gyy, gyz, gzz = np.loadtxt('data.xyz').T
predicted = np.loadtxt('predicted.txt', unpack=True)[2:]

shape = (100, 100)
data = [gyz, gzz]
titles = ['gyz', 'gzz']
for i in range(2):
    ft.vis.figure()
    ft.vis.title(titles[i])
    ft.vis.axis('scaled')
    levels = ft.vis.contourf(y, x, data[i], shape, 15, interp=True)
    ft.vis.colorbar()
    ft.vis.contour(y, x, predicted[i], shape, levels, color='k', interp=True)
    ft.vis.xlabel('East (km)')
    ft.vis.ylabel('North (km)')
    ft.vis.m2km()
ft.vis.show()

with open('result.pickle') as f:
    mesh = pickle.load(f)
with open('seeds.pickle') as f:
    seeds = pickle.load(f)
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
