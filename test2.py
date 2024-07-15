import sys
from vispy import scene
from vispy import app

canvas = scene.SceneCanvas(keys='interactive')
canvas.size = 800, 600
canvas.show()
grid = canvas.central_widget.add_grid()

cbar_widget = scene.ColorBarWidget(label="ColorBarWidget", clim=(0, 99),
                                   cmap="cool", orientation="right",
                                   border_width=1)
grid.add_widget(cbar_widget)
cbar_widget.

cbar_widget.border_color = "#212121"
grid.bgcolor = "#ffffff"

if __name__ == '__main__' and sys.flags.interactive == 0:
    app.run()