from OpenGL.GL import *
from shader import Shader
import numpy as np

# class GeometryObject:
#     def __init__(self, shader_program):
#         self.vbo = None
#         self.vao = None
#         self.shader_program = shader_program

#     def create_vbo(self, data):
#         self.vbo = glGenBuffers(1)
#         glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
#         glBufferData(GL_ARRAY_BUFFER, data.nbytes, data, GL_STATIC_DRAW)

#     def create_vao(self):
#         self.vao = glGenVertexArrays(1)
#         glBindVertexArray(self.vao)

#     def bind_vbo_to_vao(self, attribute_location, attribute_size):
#         glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
#         glVertexAttribPointer(attribute_location, attribute_size, GL_FLOAT, GL_FALSE, 0, None)
#         glEnableVertexAttribArray(attribute_location)

#     def delete(self):
#         glDeleteBuffers(1, [self.vbo])
#         glDeleteVertexArrays(1, [self.vao])


# class Triangle(GeometryObject):
#     def __init__(self, vertices, shader_program, color):
#         super().__init__(shader_program)
#         self.vertices = vertices
#         self.color = color

#         self.create_vbo(self.vertices)
#         self.create_vao()
#         self.bind_vbo_to_vao(0, 2)

#     def draw(self):
#         # Activate the shader program
#         glUseProgram(self.shader_program)
#         # Set the color uniform for the shader program
#         glUniform3f(glGetUniformLocation(self.shader_program, "color"), *self.color)

#         glBindVertexArray(self.vao)
#         glDrawArrays(GL_TRIANGLES, 0, 3)

#     def change_coordinates(self, new_vertices):
#         self.vertices = new_vertices
#         glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
#         glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)



class Line:
    def __init__(self, start, end, shader_program, color):
        self.start = start
        self.end = end
        self.shader_program = shader_program
        self.color = color
        self.linewidth = 5
        self.vao = 0
        self.vbo = 0

        self.create()

    def create(self):
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

        vertices = [self.start, self.end]
        vertices = [coord for vertex in vertices for coord in vertex]
        vertices = np.array(vertices, dtype=np.float32)

        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(0)

        glBindVertexArray(0)

    def draw(self):
        glUseProgram(self.shader_program)

        glUniform3f(glGetUniformLocation(self.shader_program, "color"), *self.color)
        glLineWidth(self.linewidth)
        glBindVertexArray(self.vao)
        glDrawArrays(GL_LINES, 0, 2)
        glBindVertexArray(0)


    def delete(self):
        glDeleteBuffers(1, [self.vbo])
        glDeleteVertexArrays(1, [self.vao])