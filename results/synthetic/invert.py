import cPickle as pickle
import numpy as np
import fatiando as ft

log = ft.log.tofile(ft.log.get(), 'invert.log')
log.info(ft.log.header())

x, y, z, gz, gzz = np.loadtxt('data.txt', unpack=True)
with open('model.pickle') as f:
    model = pickle.load(f)

bounds = [0, 600000, 0, 600000, 0, 20000]
area = bounds[:4]
shape = (50, 50)

bounds = (x.min(), x.max(), y.min(), y.max(), 0, 20000)
mesh = ft.msh.ddd.PrismMesh(bounds, (20, 60, 60))

dms = ft.pot.harvester.wrapdata(mesh, x, y, z, gz=gz, gzz=gzz)

seeds = ft.pot.harvester.sow(ft.pot.harvester.loadseeds('seeds.json'), mesh,
    mu=1000, delta=0.0001)

# How much to exagerate the 3D plot
scale = (1, 1, 10)
scalebounds = [j*scale[i/2] for i, j in enumerate(bounds)]

ft.vis.figure3d()
actor = ft.vis.prisms([s.get_prism() for s in seeds], 'density')
actor.actor.actor.scale = scale
actor = ft.vis.polyprisms(model, 'density', style='wireframe',
    cmap='gist_rainbow', linewidth=2)
actor.actor.actor.scale = scale
ft.vis.axes3d(ft.vis.outline3d(scalebounds), fmt='%.0f', nlabels=5,
    ranges=[b*0.001 for b in bounds])
ft.vis.wall_bottom(scalebounds)
ft.vis.wall_north(scalebounds)
ft.vis.show3d()

estimate, goals, misfits = ft.pot.harvester.harvest(dms, seeds)
mesh.addprop('density', estimate['density'])

with open('result.pickle', 'w') as f:
    pickle.dump(mesh, f)
with open('seeds.pickle', 'w') as f:
    pickle.dump([s.get_prism() for s in seeds], f)
output = [x, y, z]
output.extend([dm.get_predicted() for dm in dms])
np.savetxt('predicted.txt', np.transpose(output))

for dm in dms:
    ft.vis.figure()
    ft.vis.title("True: color | Inversion: contour")
    ft.vis.axis('scaled')
    levels = ft.vis.contourf(y, x, dm.data, shape, 5, interp=True)
    ft.vis.colorbar()
    ft.vis.contour(y, x, dm.get_predicted(), shape, levels, color='k',
        interp=True)
    ft.vis.xlabel('Easting (km)')
    ft.vis.ylabel('Northing (km)')
    ft.vis.m2km()
ft.vis.show()

ft.vis.figure3d()
actor = ft.vis.polyprisms(model, 'density', style='wireframe',
    cmap='gist_rainbow', linewidth=2)
actor.actor.actor.scale = scale
actor = ft.vis.prisms([s.get_prism() for s in seeds], 'density')
actor.actor.actor.scale = scale
actor = ft.vis.prisms(ft.msh.ddd.vremove(0, 'density', mesh), 'density')
actor.actor.actor.scale = scale
ft.vis.axes3d(ft.vis.outline3d(scalebounds), fmt='%.0f', nlabels=3,
    ranges=[b*0.001 for b in bounds])
ft.vis.wall_bottom(scalebounds)
ft.vis.wall_north(scalebounds)
ft.vis.show3d()

