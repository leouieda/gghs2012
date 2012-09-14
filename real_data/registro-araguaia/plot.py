import sys
import os
import fatiando as ft
import numpy as np
import cPickle as pickle

path = sys.argv[1]

y, x, data = np.loadtxt('gravity-anomaly.dat', unpack=True,
    usecols=[2, 3, 6])
predicted = np.loadtxt(os.path.join(path, 'predicted.txt'), unpack=True,
    usecols=[-1])

shape = (100, 100)
ft.vis.figure()
ft.vis.title("True: color | Inversion: contour")
ft.vis.axis('scaled')
levels = ft.vis.contourf(y, x, data, shape, 12, interp=True)
ft.vis.colorbar()
ft.vis.contour(y, x, predicted, shape, levels, color='k', interp=True)
ft.vis.plot(y, x, '.w')
ft.vis.xlabel('y (km)')
ft.vis.ylabel('x (km)')
ft.vis.show()


with open(os.path.join(path, 'result.pickle')) as f:
    mesh = pickle.load(f)
with open(os.path.join(path, 'seeds.pickle')) as f:
    seeds = pickle.load(f)
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
