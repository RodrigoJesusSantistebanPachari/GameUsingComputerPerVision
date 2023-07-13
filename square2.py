from OpenGL.GL import *
from shader import Shader
from PIL import Image
import numpy as np

class Square2:
    def __init__(self, shader_program, texture_path):
        self.shader_program = shader_program
        self.texture_path = texture_path
        self.texture = 0
        self.vertices = np.array([
            [-0.2, -0.2, 0.0, 0.0, 0.0],
            [-0.2, 0.2, 0.0, 0.0, 1.0],
            [0.2, 0.2, 0.0, 1.0, 1.0],
            [0.2, -0.2, 0.0, 1.0, 0.0]
        ], dtype=np.float32)
        self.vao = 0
        self.vbo = 0

        self.load_texture()
        self.create()

    def load_texture(self):
        # Cargar la imagen de la textura
        texture_image = Image.open(self.texture_path)
        texture_image = texture_image.transpose(Image.FLIP_TOP_BOTTOM)  # Voltear la imagen verticalmente si es necesario
        texture_data = np.array(texture_image.convert("RGBA"))  # Convertir la imagen a un arreglo NumPy

        # Crear la textura OpenGL
        self.texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, texture_data.shape[1], texture_data.shape[0], 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)
        glGenerateMipmap(GL_TEXTURE_2D)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    def create(self):
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)

        # Set vertex position attribute
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 5 * self.vertices.itemsize, None)
        glEnableVertexAttribArray(0)

        # Set texture coordinate attribute
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 5 * self.vertices.itemsize, ctypes.c_void_p(3 * self.vertices.itemsize))
        glEnableVertexAttribArray(1)

        glBindVertexArray(0)

    def draw(self):
        glUseProgram(self.shader_program)

        glUniform1i(glGetUniformLocation(self.shader_program, "texture_sampler"), 0)

        glBindTexture(GL_TEXTURE_2D, self.texture)

        glBindVertexArray(self.vao)
        glDrawArrays(GL_QUADS, 0, 4)
        glBindVertexArray(0)

    def move(self, vertice):
        print("Vertice: ", vertice)
        temp = self.vertices[:, :3] + vertice
        print("Temp: ", temp)

        if any(temp[:, 0] > 1) or any(temp[:, 0] < -1):
            vertice[0] = 0
        elif any(temp[:, 1] > 1) or any(temp[:, 1] < -1):
            vertice[1] = 0
        
        self.vertices[:, :3] += vertice

        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferSubData(GL_ARRAY_BUFFER, 0, self.vertices.nbytes, self.vertices)
        glBindBuffer(GL_ARRAY_BUFFER, 0)

    def delete(self):
        glDeleteBuffers(1, [self.vbo])
        glDeleteVertexArrays(1, [self.vao])
        glDeleteTextures(1, [self.texture])
