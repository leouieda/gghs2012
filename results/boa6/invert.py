import cPickle as pickle
import fatiando as ft
import numpy as np

log = ft.log.tofile(ft.log.get(), 'invert.log')
log.info(ft.log.header())

x, y, height, z, gxx, gxy, gxz, gyy, gyz, gzz = np.loadtxt('data.xyz').T

bounds = (x.min(), x.max(), y.min(), y.max(), -height.max(), -200)
mesh = ft.msh.ddd.PrismMesh(bounds, (23, 100, 135))
mesh.carvetopo(x, y, height)

dms = ft.pot.harvester.wrapdata(mesh, x, y, z, gyz=gyz, gzz=gzz)

seeds = ft.pot.harvester.sow(ft.pot.harvester.loadseeds('seeds.json'), mesh,
    mu=0.1, delta=0.0001)

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
output = [x, y]
output.extend([dm.get_predicted() for dm in dms])
np.savetxt('predicted.txt', np.transpose(output))

shape = (100, 100)
for dm in dms:
    ft.vis.figure()
    ft.vis.title("True: color | Inversion: contour")
    ft.vis.axis('scaled')
    levels = ft.vis.contourf(y, x, dm.data, shape, 15, interp=True)
    ft.vis.colorbar()
    ft.vis.contour(y, x, dm.get_predicted(), shape, levels, color='k',
        interp=True)
    ft.vis.xlabel('East (km)')
    ft.vis.ylabel('North (km)')
    ft.vis.m2km()
ft.vis.show()

ft.vis.figure3d()
ft.vis.prisms([s.get_prism() for s in seeds], 'density')
ft.vis.prisms(mesh, 'density')
#ft.vis.prisms(ft.msh.ddd.vremove(0, 'density', mesh), 'density')
ft.vis.axes3d(ft.vis.outline3d(bounds), fmt='%.1f', nlabels=3,
    ranges=[b*0.001 for b in bounds])
ft.vis.wall_bottom(bounds)
ft.vis.wall_north(bounds)
ft.vis.show3d()
