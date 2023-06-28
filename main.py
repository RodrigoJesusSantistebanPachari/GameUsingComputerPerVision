import glfw
from OpenGL.GL import *
from util import init_glfw, delete_resources, np_array
from constants import *
from shader import Shader
from geometry import Line
from hand import Hand
import numpy as np


def main():
    window = init_glfw()

    # Create the shader program
    shader_program = Shader(vertex_shader_source, fragment_shader_source)

   # Create the hand object
    hand_color = [0.91, 0.75, 0.67] # skin color
    hand = Hand(shader_program.get_program_number(), hand_color)
    
    counter = 0

    # Main loop
    while not glfw.window_should_close(window):
        # Clear the color buffer
        glClear(GL_COLOR_BUFFER_BIT)

        counter += 1
        if counter > 100000:
            counter = 0
        # Draw the hand
        hand.draw()

        if counter % 500 == 0:
            hand.move(3.0)

        # Swap buffers
        glfw.swap_buffers(window)
        # Poll events
        glfw.poll_events()

    # Clean up resources
    hand.delete()
    # Terminate GLFW
    glfw.terminate()


if __name__ == '__main__':
    main()
