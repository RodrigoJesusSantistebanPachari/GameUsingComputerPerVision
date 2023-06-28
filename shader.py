from OpenGL.GL import *


class Shader:
    def __init__(self, vertex_source, fragment_source):
        self.vertex_source = vertex_source
        self.fragment_source = fragment_source
        self.shader_program = None
        self.compile()

    def compile(self):
        vertex_shader = glCreateShader(GL_VERTEX_SHADER)
        glShaderSource(vertex_shader, self.vertex_source)
        glCompileShader(vertex_shader)

        # Check vertex shader compilation status
        if not glGetShaderiv(vertex_shader, GL_COMPILE_STATUS):
            error = glGetShaderInfoLog(vertex_shader).decode()
            raise RuntimeError(f"Vertex shader compilation failed: {error}")

        fragment_shader = glCreateShader(GL_FRAGMENT_SHADER)
        glShaderSource(fragment_shader, self.fragment_source)
        glCompileShader(fragment_shader)

        # Check fragment shader compilation status
        if not glGetShaderiv(fragment_shader, GL_COMPILE_STATUS):
            error = glGetShaderInfoLog(fragment_shader).decode()
            raise RuntimeError(f"Fragment shader compilation failed: {error}")

        self.shader_program = glCreateProgram()
        glAttachShader(self.shader_program, vertex_shader)
        glAttachShader(self.shader_program, fragment_shader)
        glLinkProgram(self.shader_program)

        # Check shader program linking status
        if not glGetProgramiv(self.shader_program, GL_LINK_STATUS):
            error = glGetProgramInfoLog(self.shader_program).decode()
            raise RuntimeError(f"Shader program linking failed: {error}")

        glDeleteShader(vertex_shader)
        glDeleteShader(fragment_shader)

    def use(self):
        glUseProgram(self.shader_program)

    def get_program_number(self):
        return self.shader_program

    def delete(self):
        glDeleteProgram(self.shader_program)
