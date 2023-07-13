from OpenGL.GL import *
from shader import Shader
import numpy as np

class Cube:
    def __init__(self, shader_program, color):
        self.shader_program = shader_program
        self.color = color
        self.vertices = np.array([
            # Front face
            [-0.2, -0.2, 0.2],
            [-0.2, 0.2, 0.2],
            [0.2, 0.2, 0.2],
            [0.2, -0.2, 0.2],
            # Back face
            [-0.2, -0.2, -0.2],
            [-0.2, 0.2, -0.2],
            [0.2, 0.2, -0.2],
            [0.2, -0.2, -0.2],
            # Top face
            [-0.2, 0.2, -0.2],
            [-0.2, 0.2, 0.2],
            [0.2, 0.2, 0.2],
            [0.2, 0.2, -0.2],
            # Bottom face
            [-0.2, -0.2, -0.2],
            [-0.2, -0.2, 0.2],
            [0.2, -0.2, 0.2],
            [0.2, -0.2, -0.2],
            # Right face
            [0.2, -0.2, -0.2],
            [0.2, 0.2, -0.2],
            [0.2, 0.2, 0.2],
            [0.2, -0.2, 0.2],
            # Left face
            [-0.2, -0.2, -0.2],
            [-0.2, 0.2, -0.2],
            [-0.2, 0.2, 0.2],
            [-0.2, -0.2, 0.2]
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
        glDrawArrays(GL_QUADS, 0, 24)  # 24 vertices for the cube (6 faces * 4 vertices)
        glBindVertexArray(0)

    def move(self, vertice):
        print("Vertice: ", vertice)
        temp = self.vertices + vertice
        print("Temp: ", temp)

        if any(temp[:, 0] > 1) or any(temp[:, 0] < -1):
            vertice[0] = 0
        elif any(temp[:, 1] > 1) or any(temp[:, 1] < -1):
            vertice[1] = 0
        
        
        self.vertices += vertice

        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferSubData(GL_ARRAY_BUFFER, 0, self.vertices.nbytes, self.vertices)
        glBindBuffer(GL_ARRAY_BUFFER, 0)

    def delete(self):
        glDeleteBuffers(1, [self.vbo])
        glDeleteVertexArrays(1, [self.vao])
