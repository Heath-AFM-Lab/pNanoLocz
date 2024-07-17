import numpy as np
import vispy.scene
from vispy import app

# Generate a random image using NumPy
image_data = np.random.rand(100, 100, 3).astype(np.float32)  # Example image size: 100x100, float32

# Create a canvas with size matching the image dimensions
canvas = vispy.scene.SceneCanvas(keys='interactive', show=True, size=(image_data.shape[1], image_data.shape[0]))

# Create a viewbox to display the image
view = canvas.central_widget.add_view()

# Create an Image visual
image = vispy.scene.visuals.Image(image_data, parent=view.scene, method='auto')

# Adjust camera to fit the image without padding
view.camera = vispy.scene.cameras.PanZoomCamera(aspect=1)
view.camera.set_range((0, image_data.shape[1]), (0, image_data.shape[0]))

# Disable viewbox margins (if applicable)
view.camera.rect = (0, 0, image_data.shape[1], image_data.shape[0])

# Start the Vispy app
if __name__ == '__main__':
    app.run()
