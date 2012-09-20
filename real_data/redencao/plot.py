import fatiando as ft
import numpy as np
import cPickle as pickle

outcropx, outcropy = np.loadtxt('outcrop.txt', unpack=True)
x, y, data = np.loadtxt('data.xyz', unpack=True)
predicted = np.loadtxt('predicted.txt', unpack=True, usecols=[-1])

shape = (100, 100)
ft.vis.figure()
ft.vis.title("True: color | Inversion: contour")
ft.vis.axis('scaled')
levels = ft.vis.contourf(y, x, data, shape, 12, interp=True)
ft.vis.colorbar()
ft.vis.contour(y, x, predicted, shape, levels, color='k', interp=True)
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
ft.vis.prisms(ft.msh.ddd.vremove(0, 'density', mesh), 'density')
ft.vis.vtk.mlab.plot3d(outcropx, outcropy, np.zeros_like(outcropx),
    color=(1,0,0), tube_radius=300)
ft.vis.axes3d(ft.vis.outline3d(bounds), fmt='%.1f', nlabels=3,
    ranges=[b*0.001 for b in bounds])
ft.vis.wall_bottom(bounds)
ft.vis.wall_north(bounds)
ft.vis.show3d()
