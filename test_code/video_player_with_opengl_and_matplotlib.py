import sys
import numpy as np
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QWidget
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QSurfaceFormat
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader


vertex_shader_source = """
#version 330
in vec2 position;
in vec2 texcoord;
out vec2 Texcoord;
void main() {
    Texcoord = texcoord;
    gl_Position = vec4(position, 0.0, 1.0);
}
"""

fragment_shader_source = """
#version 330
in vec2 Texcoord;
out vec4 outColor;
uniform sampler2D tex;
void main() {
    outColor = texture(tex, Texcoord);
}
"""


class SimpleOpenGLWidget(QOpenGLWidget):
    def __init__(self, video_frames, parent=None):
        super().__init__(parent)
        self.video_frames = video_frames
        self.current_frame_index = 0

        # Setup a timer to update the frames
        self.timer = QTimer()
        self.timer.timeout.connect(self._go_to_next_frame)
        self.set_fps(30)
        self.timer.start()

    def initializeGL(self):
        self.program = compileProgram(
            compileShader(vertex_shader_source, GL_VERTEX_SHADER),
            compileShader(fragment_shader_source, GL_FRAGMENT_SHADER)
        )

        self.vertex_data = np.array([
            # Positions    # Texture coords
            -1.0,  1.0,    0.0, 1.0,
            -1.0, -1.0,    0.0, 0.0,
             1.0, -1.0,    1.0, 0.0,
             1.0,  1.0,    1.0, 1.0,
        ], dtype=np.float32)

        self.indices = np.array([0, 1, 2, 2, 3, 0], dtype=np.uint32)

        self.vbo = glGenBuffers(1)
        self.ebo = glGenBuffers(1)
        self.vao = glGenVertexArrays(1)

        glBindVertexArray(self.vao)

        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, self.vertex_data.nbytes, self.vertex_data, GL_STATIC_DRAW)

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ebo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.indices.nbytes, self.indices, GL_STATIC_DRAW)

        position = glGetAttribLocation(self.program, 'position')
        glEnableVertexAttribArray(position)
        glVertexAttribPointer(position, 2, GL_FLOAT, GL_FALSE, 4 * self.vertex_data.itemsize, ctypes.c_void_p(0))

        texcoord = glGetAttribLocation(self.program, 'texcoord')
        glEnableVertexAttribArray(texcoord)
        glVertexAttribPointer(texcoord, 2, GL_FLOAT, GL_FALSE, 4 * self.vertex_data.itemsize, ctypes.c_void_p(2 * self.vertex_data.itemsize))

        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

        self.texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        glBindTexture(GL_TEXTURE_2D, 0)

    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT)
        self._render_frame(self.video_frames[self.current_frame_index])

    def _render_frame(self, frame):
        height, width, _ = frame.shape
        frame = np.flipud(frame)

        glBindTexture(GL_TEXTURE_2D, self.texture)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, frame)
        glBindTexture(GL_TEXTURE_2D, 0)

        glUseProgram(self.program)

        glBindVertexArray(self.vao)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)
        glBindTexture(GL_TEXTURE_2D, 0)
        glBindVertexArray(0)

        glUseProgram(0)

    def _go_to_next_frame(self):
        self.current_frame_index = (self.current_frame_index + 1) % len(self.video_frames)
        self.update()

    def set_fps(self, fps):
        self.fps = fps
        interval = 1000 // self.fps
        self.timer.setInterval(interval)


if __name__ == '__main__':
    video_frames = (np.random.rand(100, 100, 100, 3) * 255).astype(np.uint8)

    app = QApplication(sys.argv)

    main_window = QWidget()
    layout = QVBoxLayout(main_window)

    format = QSurfaceFormat()
    format.setProfile(QSurfaceFormat.OpenGLContextProfile.CoreProfile)
    format.setVersion(3, 3)

    opengl_widget = SimpleOpenGLWidget(video_frames)
    opengl_widget.setFormat(format)

    layout.addWidget(opengl_widget)

    main_window.setWindowTitle('Simple OpenGL Video Player')
    main_window.show()

    sys.exit(app.exec())
