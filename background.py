import glfw
from OpenGL.GL import *
from PIL import Image

class Background:
    def __init__(self, shader_program, window_width, window_height, texture_path):
        self.window_width = window_width
        self.window_height = window_height
        self.shader_program = shader_program
        self.texture_id = self.load_texture(texture_path)

    def load_texture(self, file_path):
        image = Image.open(file_path)
        flipped_image = image.transpose(Image.FLIP_TOP_BOTTOM)
        
        width, height = flipped_image.size
        texture_data = flipped_image.convert("RGBA").tobytes()

        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)
        glGenerateMipmap(GL_TEXTURE_2D)

        return texture_id

    def draw(self):
        glUseProgram(self.shader_program)

        glBindTexture(GL_TEXTURE_2D, self.texture_id)

        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0)
        glVertex2f(-0.5, 0.5)  # Top-left vertex

        glTexCoord2f(1.0, 0.0)
        glVertex2f(0.5, 0.5)   # Top-right vertex

        glTexCoord2f(1.0, 1.0)
        glVertex2f(0.5, -0.5)  # Bottom-right vertex

        glTexCoord2f(0.0, 1.0)
        glVertex2f(-0.5, -0.5) # Bottom-left vertex
        glEnd()
