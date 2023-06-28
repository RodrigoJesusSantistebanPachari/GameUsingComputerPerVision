from OpenGL.GL import *
from shader import Shader
import numpy as np

class Square:
    def __init__(self, shader_program, color):
        self.shader_program = shader_program
        self.color = color
        self.vertices = np.array([
            [-0.2, -0.2, 0.0],
            [-0.2, 0.2, 0.0],
            [0.2, 0.2, 0.0],
            [0.2, -0.2, 0.0]
        ], dtype=np.float32)
        self.vao = 0
        self.vbo = 0

        self.create()

    def create(self):
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)

        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(0)

        glBindVertexArray(0)

    def draw(self):
        glUseProgram(self.shader_program)

        glUniform3f(glGetUniformLocation(self.shader_program, "color"), *self.color)
        glBindVertexArray(self.vao)
        glDrawArrays(GL_QUADS, 0, 4)
        glBindVertexArray(0)

    def move(self, vertice):
        # Move the square randomly
        random_translation = (np.random.rand(3) - 0.5) * 0.1

        print("Random trnslation: ", random_translation)
        print("Vertice: ", vertice)

        self.vertices += vertice
        print("Final vertices: ", self.vertices)

        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferSubData(GL_ARRAY_BUFFER, 0, self.vertices.nbytes, self.vertices)
        glBindBuffer(GL_ARRAY_BUFFER, 0)

    def delete(self):
        glDeleteBuffers(1, [self.vbo])
        glDeleteVertexArrays(1, [self.vao])
