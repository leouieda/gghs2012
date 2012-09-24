import numpy as np
import fatiando as ft

x = np.arange(0, 50)
z = np.zeros_like(x)
area = (0, 50, 0, 50)
app = ft.ui.gui.Moulder(area, x, z)
app.run()
data = app.get_data()
app = ft.ui.gui.Moulder(area, x, z, data)
app.run()
