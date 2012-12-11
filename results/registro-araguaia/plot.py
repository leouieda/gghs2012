import sys
import os
import fatiando as ft
import numpy as np
import cPickle as pickle

path = sys.argv[1]

y, x, data = np.loadtxt('gravity-anomaly.dat', unpack=True,
    usecols=[2, 3, 6])
y, x = y*1000, x*1000
predicted = np.loadtxt(os.path.join(path, 'predicted.txt'), unpack=True,
    usecols=[-1])

with open(os.path.join(path, 'seeds.pickle')) as f:
    seeds = pickle.load(f)
sx, sy = np.transpose([s.center()[:2] for s in seeds])

fmt = '.pdf'
dpi = 200
size = (5.6, 4)
shape = (200, 200)
#
#ft.vis.figure(figsize=size)
#ft.vis.subplots_adjust(bottom=0.12)
#ft.vis.title("Bouguer anomaly")
#ft.vis.axis('scaled')
#levels = ft.vis.contourf(y, x, data, shape, 20, interp=True)
#cb = ft.vis.colorbar(shrink=0.86)
#cb.set_label('mGal')
#ft.vis.plot(y, x, 'xk')
#ft.vis.xlabel('East (km)')
#ft.vis.ylabel('North (km)')
#ft.vis.m2km()
#ft.vis.savefig('gz' + fmt, dpi=dpi)

ft.vis.figure(figsize=size)
ft.vis.title("Residuals")
ft.vis.axis('scaled')
ft.vis.hist(data - predicted, nbins=5)
ft.vis.xlabel('East (km)')
ft.vis.ylabel('North (km)')
ft.vis.m2km()
ft.vis.savefig('gz' + fmt, dpi=dpi)

ft.vis.figure(figsize=size)
ft.vis.subplots_adjust(bottom=0.12)
ft.vis.title("Bouguer anomaly")
ft.vis.axis('scaled')
levels = ft.vis.contourf(y, x, data, shape, 20, interp=True)
cb = ft.vis.colorbar(shrink=0.86)
cb.set_label('mGal')
ft.vis.plot(sy, sx, 'ok', markersize=8)
ft.vis.plot(y, x, 'xk')
ft.vis.xlabel('East (km)')
ft.vis.ylabel('North (km)')
ft.vis.m2km()
ft.vis.savefig('gz_seed' + fmt, dpi=dpi)

ft.vis.figure(figsize=size)
ft.vis.subplots_adjust(bottom=0.12)
ft.vis.title("Bouguer anomaly")
ft.vis.axis('scaled')
levels = ft.vis.contourf(y, x, data, shape, 12, interp=True)
cb = ft.vis.colorbar(shrink=0.86)
cb.set_label('mGal')
ft.vis.contour(y, x, predicted, shape, levels, color='k', interp=True,
    linewidth=1.5)
ft.vis.plot(y, x, 'xk')
ft.vis.xlabel('East (km)')
ft.vis.ylabel('North (km)')
ft.vis.m2km()
ft.vis.savefig('gz_fit' + fmt, dpi=dpi)

#ft.vis.show()


with open(os.path.join(path, 'result.pickle')) as f:
    mesh = pickle.load(f)
bounds = mesh.bounds

def setview(scene):
    scene.scene.camera.position = [4798.328726633199, -14151.146038974042, -257.13993504205513]
    scene.scene.camera.focal_point = [74356.368529307525, 39415.820849083844, 17862.818922753184]
    scene.scene.camera.view_angle = 30.0
    scene.scene.camera.view_up = [0.16217628303946111, 0.12069320626390098, -0.97935284917196408]
    scene.scene.camera.clipping_range = [23847.181091153507, 171909.1769857296]
    scene.scene.camera.compute_view_plane_normal()
    scene.scene.render()

scene = ft.vis.figure3d(size=(1300, 800))
ft.vis.prisms(ft.msh.ddd.vremove(0, 'density', mesh), 'density')
ft.vis.outline3d(bounds)
ft.vis.wall_bottom(bounds)
ft.vis.wall_north(bounds)
setview(scene)
ft.vis.savefig3d('result.png')

scene = ft.vis.figure3d(size=(1300, 800))
ft.vis.prisms(seeds, 'density')
ft.vis.outline3d(bounds)
ft.vis.wall_bottom(bounds)
ft.vis.wall_north(bounds)
setview(scene)
ft.vis.savefig3d('seeds.png')

scene = ft.vis.figure3d(size=(1300, 800))
ft.vis.prisms(seeds, 'density').actor.actor.visibility = 0
ft.vis.axes3d(ft.vis.outline3d(bounds), fmt='%.1f', nlabels=3,
    ranges=[b*0.001 for b in bounds])
setview(scene)
ft.vis.savefig3d('axes.pdf')

ft.vis.show3d()
