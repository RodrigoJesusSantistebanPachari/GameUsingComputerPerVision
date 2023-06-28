import glfw
import numpy as np


# Callback function for keyboard input
def key_callback(window, key, scancode, action, mods):
    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window, True)

def init_glfw():
    # Initialize GLFW
    if not glfw.init():
        return

    # Create a window
    window = glfw.create_window(800, 600, "OpenGL Window", None, None)
    if not window:
        glfw.terminate()
        return

    # Set the window as the current OpenGL context
    glfw.make_context_current(window)

    # Set the callback function for keyboard input
    glfw.set_key_callback(window, key_callback)

    return window

def delete_resources(*args):
    for arg in args:
        arg.delete()
        

def np_array(data):
    return np.array(data, dtype=np.float32)