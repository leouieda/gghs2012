import fatiando as ft
import numpy as np
import cPickle as pickle

outcropy, outcropx = np.loadtxt('outcrop.txt', unpack=True)
lon, lat, data = np.loadtxt('gravity-anomaly-residual.dat', unpack=True,
    usecols=[0, 1, -1])
predicted = np.loadtxt('predicted.txt', unpack=True, usecols=[-1])

shape = (100, 100)
ft.vis.figure()
ft.vis.title("True: color | Inversion: contour")
ft.vis.axis('scaled')
levels = ft.vis.contourf(lon, lat, data, shape, 12, interp=True)
ft.vis.colorbar()
ft.vis.contour(lon, lat, predicted, shape, levels, color='k', interp=True)
ft.vis.xlabel('Longitude')
ft.vis.ylabel('Latitude')
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
#ft.vis.prisms(mesh, 'density')
ft.vis.vtk.mlab.plot3d(outcropx*111000, outcropy*111000,
    bounds[-2]*np.ones_like(outcropx), color=(1,0,0), tube_radius=300)
ft.vis.axes3d(ft.vis.outline3d(bounds), fmt='%.1f', nlabels=3,
    ranges=[lat.min(), lat.max(), lon.min(), lon.max(), bounds[-2]*0.001,
        bounds[-1]*0.001])
ft.vis.wall_bottom(bounds)
ft.vis.wall_north(bounds)
ft.vis.show3d()
