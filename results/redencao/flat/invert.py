import cPickle as pickle
import fatiando as ft
import numpy as np

log = ft.log.tofile(ft.log.get(), 'invert.log')
log.info(ft.log.header())

outcropx, outcropy = np.loadtxt('../outcrop.xyz', unpack=True)
x, y, data = np.loadtxt('../data.xyz', unpack=True)
z = -0.1*np.ones_like(x)

pad = 5000
bounds = [x.min() - pad, x.max() + pad, y.min() - pad, y.max() + pad, 0, 10000]
#mesh = ft.msh.ddd.PrismMesh(bounds, (60, 56, 64))
mesh = ft.msh.ddd.PrismMesh(bounds, (30, 28, 32))

dms = ft.pot.harvester.wrapdata(mesh, x, y, z, gz=data)

seeds = ft.pot.harvester.sow(ft.pot.harvester.loadseeds('seeds.json'), mesh,
    mu=0.5, delta=0.00001)

ft.vis.figure3d()
ft.vis.prisms([s.get_prism() for s in seeds], 'density')
ft.vis.vtk.mlab.plot3d(outcropx, outcropy, np.zeros_like(outcropx),
    color=(1,0,0), tube_radius=300)
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
np.savetxt('predicted.txt', np.transpose([x, y, predicted]))

# Compute the length/width and width thickness ratios
body = ft.msh.ddd.vremove(0, 'density', mesh)
length = max(p.x2 for p in body) - min(p.x1 for p in body)
width = max(p.y2 for p in body) - min(p.y1 for p in body)
thickness = max(p.z2 for p in body) - min(p.z1 for p in body)
LW = length/width
WT = width/thickness
ratio = LW/WT
log.info("Dimensions of estimate:")
log.info("length = %g" % (length))
log.info("width  = %g" % (width))
log.info("thick  = %g" % (thickness))
log.info("L/W    = %g" % (LW))
log.info("W/T    = %g" % (WT))
log.info("ratio  = %g" % (ratio))

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

ft.vis.figure()
ft.vis.title("Residuals")
ft.vis.hist(data - predicted, bins=8, color='grey')
ft.vis.xlabel('Residuals (mGal)')
ft.vis.ylabel('Count')

ft.vis.show()

ft.vis.figure3d()
ft.vis.prisms([s.get_prism() for s in seeds], 'density')
ft.vis.prisms(body, 'density')
ft.vis.vtk.mlab.plot3d(outcropx, outcropy, np.zeros_like(outcropx),
    color=(1,0,0), tube_radius=300)
ft.vis.axes3d(ft.vis.outline3d(bounds), fmt='%.1f', nlabels=5,
    ranges=[b*0.001 for b in bounds])
ft.vis.wall_bottom(bounds)
ft.vis.wall_north(bounds)
ft.vis.show3d()
