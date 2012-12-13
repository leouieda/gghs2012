import cPickle as pickle
import fatiando as ft
import numpy as np

log = ft.log.tofile(ft.log.get(), 'invert.log')
log.info(ft.log.header())

outcropy, outcropx = np.loadtxt('outcrop.txt', unpack=True)*111000
lon, lat, height, data = np.loadtxt('gravity-anomaly-residual.dat', unpack=True)
z = -height
y, x = lon*111000, lat*111000

bounds = (x.min(), x.max(), y.min(), y.max(), z.min() + 1, 15000)
#mesh = ft.msh.ddd.PrismMesh(bounds, (30, 70, 70))
mesh = ft.msh.ddd.PrismMesh(bounds, (10, 30, 30))
mesh.carvetopo(x, y, height)

dms = ft.pot.harvester.wrapdata(mesh, x, y, z, gz=data)

mu, delta = 1, 0.000001
seeds = ft.pot.harvester.sow(ft.pot.harvester.loadseeds('seeds-larger.json'),
    mesh, mu=mu, delta=delta)
seeds.extend(
    ft.pot.harvester.sow(ft.pot.harvester.loadseeds('seeds-smaller.json'),
        mesh, mu=mu, delta=delta))

ft.vis.figure3d()
ft.vis.prisms([s.get_prism() for s in seeds], 'density')
ft.vis.vtk.mlab.plot3d(outcropx, outcropy, z.min()*np.ones_like(outcropx),
    color=(1,0,0), tube_radius=300)
ft.vis.axes3d(ft.vis.outline3d(bounds), fmt='%.1f', nlabels=3,
    ranges=[lat.min(), lat.max(), lon.min(), lon.max(), bounds[-2]*0.001,
        bounds[-1]*0.001])
ft.vis.wall_bottom(bounds)
ft.vis.wall_north(bounds)
ft.vis.show3d()

estimate, goals, misfits = ft.pot.harvester.harvest(dms, seeds)
mesh.addprop('density', estimate['density'])
predicted = dms[0].get_predicted()

with open('result.pickle', 'w') as f:
    pickle.dump(mesh, f)
with open('seeds.pickle', 'w') as f:
    pickle.dump([s.get_prism() for s in seeds], f)
np.savetxt('predicted.txt', np.transpose([lon, lat, predicted]))

shape = (100, 100)
ft.vis.figure()
ft.vis.title("True: color | Inversion: contour")
ft.vis.axis('scaled')
levels = ft.vis.contourf(lon, lat, data, shape, 20, interp=True)
ft.vis.colorbar()
ft.vis.contour(lon, lat, predicted, shape, levels, color='k', interp=True)
ft.vis.xlabel('Longitude')
ft.vis.ylabel('Latitude')
ft.vis.m2km()
ft.vis.show()

ft.vis.figure3d()
ft.vis.prisms([s.get_prism() for s in seeds], 'density')
ft.vis.prisms(ft.msh.ddd.vremove(0, 'density', mesh), 'density')
#ft.vis.prisms(mesh, 'density')
ft.vis.vtk.mlab.plot3d(outcropx, outcropy, z.min()*np.ones_like(outcropx),
    color=(1,0,0), tube_radius=300)
ft.vis.axes3d(ft.vis.outline3d(bounds), fmt='%.1f', nlabels=3,
    ranges=[lat.min(), lat.max(), lon.min(), lon.max(), bounds[-2]*0.001,
        bounds[-1]*0.001])
ft.vis.wall_bottom(bounds)
ft.vis.wall_north(bounds)
ft.vis.show3d()
