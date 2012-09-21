import fatiando as ft
import numpy as np
import cPickle as pickle

log = ft.log.get()
log.info(ft.log.header())
log.info(__doc__)

bounds = [0, 600000, 0, 600000, 0, 20000]
area = bounds[:4]

log.info("GENERATING SYNTHETIC DATA")
axes = ft.vis.figure().gca()
ft.vis.axis('scaled')
density = 300
model = [
    ft.msh.ddd.PolygonalPrism(
        ft.ui.picker.draw_polygon(area, axes, xy2ne=True),
        1000, 9000, {'density':density})]
# Calculate the data
shape = (50, 50)
xp, yp, zp = ft.grd.regular(area, shape, z=-4000)
gz = ft.utils.contaminate(ft.pot.polyprism.gz(xp, yp, zp, model), 0.1)
gzz = ft.utils.contaminate(ft.pot.polyprism.gzz(xp, yp, zp, model), 1)
# and plot it
data = [gz, gzz]
titles = ['gz (mGal)', 'gzz (Eotvos)']
ft.vis.figure(figsize=(12,5))
for i in range(2):
    ft.vis.subplot(1, 2, i + 1)
    ft.vis.axis('scaled')
    ft.vis.title(titles[i])
    ft.vis.contourf(yp, xp, data[i], shape, 20)
    ft.vis.colorbar()
    ft.vis.polygon(model[0], '.-k', xy2ne=True)
    ft.vis.set_area(area)
    ft.vis.m2km()
    ft.vis.xlabel("Easting (km)")
    ft.vis.ylabel("Northing (km)")
ft.vis.show()

np.savetxt('data.txt', np.transpose([xp, yp, zp, gz, gzz]))
with open('model.pickle', 'w') as f:
    pickle.dump(model, f)

# Show the model
ft.vis.figure3d()
ft.vis.polyprisms(model, 'density')
ft.vis.axes3d(ft.vis.outline3d(bounds), ranges=[b*0.001 for b in bounds],
    fmt='%.0f')
ft.vis.wall_bottom(bounds)
ft.vis.wall_north(bounds)
ft.vis.show3d()
