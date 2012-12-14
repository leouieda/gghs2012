import sys
import fatiando as ft
import numpy as np
import cPickle as pickle

path = sys.argv[1]

outcropx, outcropy = np.loadtxt('outcrop.xyz', unpack=True)
x, y, data = np.loadtxt('data.xyz', unpack=True)
predicted = np.loadtxt('%s/predicted.txt' % (path), unpack=True, usecols=[-1])

with open('%s/seeds.pickle' % (path)) as f:
    seeds = pickle.load(f)
sx, sy = np.transpose([s.center()[:2] for s in seeds])

fmt = '.pdf'
dpi = 200
size = (5.6, 4)
shape = (200, 200)

ft.vis.figure(figsize=size)
ft.vis.subplots_adjust(bottom=0.12)
ft.vis.title("Bouguer anomaly")
ft.vis.axis('scaled')
levels = ft.vis.contourf(y, x, data, shape, 12, interp=True)
cb = ft.vis.colorbar()
cb.set_label('mGal')
ft.vis.plot(outcropy, outcropx, '-r', linewidth=3)
ft.vis.xlabel('East (km)')
ft.vis.ylabel('North (km)')
ft.vis.m2km()
ft.vis.savefig('%s/gz' % (path) + fmt, dpi=dpi)

ft.vis.figure(figsize=size)
ft.vis.title("Residuals")
ft.vis.hist(data - predicted, bins=8, color='grey')
ft.vis.xlabel('Residuals (mGal)')
ft.vis.ylabel('Number')
ft.vis.savefig('%s/residuals' % (path) + fmt, dpi=dpi)

ft.vis.figure(figsize=size)
ft.vis.subplots_adjust(bottom=0.12)
ft.vis.title("Bouguer anomaly")
ft.vis.axis('scaled')
levels = ft.vis.contourf(y, x, data, shape, 12, interp=True)
cb = ft.vis.colorbar()
cb.set_label('mGal')
ft.vis.plot(outcropy, outcropx, '-r', linewidth=3)
ft.vis.plot(sy, sx, 'ok', markersize=10)
ft.vis.xlabel('East (km)')
ft.vis.ylabel('North (km)')
ft.vis.m2km()
ft.vis.savefig('%s/gz_seed' % (path) + fmt, dpi=dpi)

ft.vis.figure(figsize=size)
ft.vis.subplots_adjust(bottom=0.12)
ft.vis.title("Bouguer anomaly")
ft.vis.axis('scaled')
levels = ft.vis.contourf(y, x, data, shape, 6, interp=True)
cb = ft.vis.colorbar()
cb.set_label('mGal')
ft.vis.contour(y, x, predicted, shape, levels, color='k', interp=True,
    linewidth=2)
ft.vis.xlabel('East (km)')
ft.vis.ylabel('North (km)')
ft.vis.m2km()
ft.vis.savefig('%s/gz_fit' % (path) + fmt, dpi=dpi)

#ft.vis.show()

with open('%s/result.pickle' % (path)) as f:
    mesh = pickle.load(f)
bounds = mesh.bounds

def setview1(scene):
    scene.scene.camera.position = [8970369.726345323, 546739.13708759774, -48094.14263369923]
    scene.scene.camera.focal_point = [9096408.0507883951, 605453.3671516024, 28797.705195244191]
    scene.scene.camera.view_angle = 30.0
    scene.scene.camera.view_up = [0.44341068784091225, 0.19411351245684388, -0.87504680228552112]
    scene.scene.camera.clipping_range = [63995.729393094967, 279160.77435654443]
    scene.scene.camera.compute_view_plane_normal()
    scene.scene.render()

def setview2(scene):
    scene.scene.camera.position = [9099042.4104312118, 761180.63646937313, 1284.6908519542119]
    scene.scene.camera.focal_point = [9104425.2919641305, 605053.39346629032, 30279.257267563007]
    scene.scene.camera.view_angle = 30.0 
    scene.scene.camera.view_up = [0.0044203337334183697, -0.18244008558386604, -0.98320703609251958]
    scene.scene.camera.clipping_range = [87872.259905739993, 244743.13653317251]
    scene.scene.camera.compute_view_plane_normal()
    scene.scene.render()

def setview3(scene):
    scene.scene.parallel_projection = True
    scene.scene.camera.position = [9101868.4334705323, 600226.74961825833, -172125.63471488922]
    scene.scene.camera.focal_point = [9101868.4334705323, 600226.74961825833, 4826.7949218750009]
    scene.scene.camera.view_angle = 30.0
    scene.scene.camera.view_up = [0.99999972704944473, 0.00073885115968195961, 0.0]
    scene.scene.camera.clipping_range = [164888.22723492782, 192565.59480201881]
    scene.scene.camera.compute_view_plane_normal()
    scene.scene.render()

size = (1200, 1000)

scene = ft.vis.figure3d(size=size)
ft.vis.prisms(seeds, 'density').actor.actor.visibility = 0
ft.vis.axes3d(ft.vis.outline3d(bounds), fmt='%.1f', nlabels=3,
    ranges=[b*0.001 for b in bounds])
setview1(scene)
ft.vis.savefig3d('%s/axes1.pdf' % (path))
setview2(scene)
ft.vis.savefig3d('%s/axes2.pdf' % (path))
setview3(scene)
ft.vis.savefig3d('%s/axes3.pdf' % (path))

scene = ft.vis.figure3d(size=size)
ft.vis.vtk.mlab.plot3d(outcropx, outcropy, np.zeros_like(outcropx),
    color=(1,0,0), tube_radius=400)
ft.vis.prisms(ft.msh.ddd.vremove(0, 'density', mesh), 'density')
ft.vis.outline3d(bounds)
ft.vis.wall_bottom(bounds)
ft.vis.wall_north(bounds)
setview1(scene)
ft.vis.savefig3d('%s/result1.png' % (path))
setview2(scene)
ft.vis.savefig3d('%s/result2.png' % (path))

scene = ft.vis.figure3d(size=size)
ft.vis.vtk.mlab.plot3d(outcropx, outcropy, np.zeros_like(outcropx),
    color=(1,0,0), tube_radius=300)
ft.vis.prisms(seeds, 'density')
ft.vis.outline3d(bounds)
ft.vis.wall_bottom(bounds)
ft.vis.wall_north(bounds)
setview1(scene)
ft.vis.savefig3d('%s/seeds1.png' % (path))
setview2(scene)
ft.vis.savefig3d('%s/seeds2.png' % (path))

scene = ft.vis.figure3d(size=size)
ft.vis.vtk.mlab.plot3d(outcropx, outcropy, np.zeros_like(outcropx),
    color=(1,0,0), tube_radius=400)
ft.vis.prisms(ft.msh.ddd.vremove(0, 'density', mesh.get_layer(0)), 'density')
ft.vis.outline3d(bounds)
setview3(scene)
ft.vis.savefig3d('%s/result3.png' % (path))

ft.vis.show3d()



