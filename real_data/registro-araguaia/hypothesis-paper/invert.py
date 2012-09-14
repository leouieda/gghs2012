import cPickle as pickle
import fatiando as ft
import numpy as np

log = ft.log.tofile(ft.log.get(), 'invert.log')
log.info(ft.log.header())

y, x, height, data = np.loadtxt('../gravity-anomaly.dat', unpack=True,
    usecols=[2, 3, 4, 6])
# Convert from km to m
x, y = x*1000, y*1000
z = -height

bounds = (x.min(), x.max(), y.min(), y.max(), z.min() + 1, 25000)
mesh = ft.msh.ddd.PrismMesh(bounds, (25, 50, 40))
mesh.carvetopo(x, y, height)

dms = ft.pot.harvester.wrapdata(mesh, x, y, z, gz=data)

seeds = ft.pot.harvester.sow(ft.pot.harvester.loadseeds('seeds.json'),
    mesh, mu=0.1, delta=0.00001)

ft.vis.figure3d()
ft.vis.prisms([s.get_prism() for s in seeds], 'density')
ft.vis.axes3d(ft.vis.outline3d(bounds), fmt='%.1f', nlabels=3,
    ranges=[b*0.001 for b in bounds])
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
np.savetxt('predicted.txt', np.transpose([y, x, predicted]))

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
ft.vis.m2km()
ft.vis.show()

ft.vis.figure3d()
ft.vis.prisms([s.get_prism() for s in seeds], 'density')
ft.vis.prisms(ft.msh.ddd.vremove(0, 'density', mesh), 'density')
#ft.vis.prisms(mesh, 'density')
ft.vis.axes3d(ft.vis.outline3d(bounds), fmt='%.1f', nlabels=3,
    ranges=[b*0.001 for b in bounds])
ft.vis.wall_bottom(bounds)
ft.vis.wall_north(bounds)
ft.vis.show3d()
