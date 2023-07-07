# OpenGL and GLFW libraries
import glfw
from OpenGL.GL import *
from util import init_glfw, delete_resources, np_array
from constants import *
from shader import Shader
from geometry import Line
from hand import Hand
from square import Square
from background import Background
import numpy as np

# OpenCV and mediapipe libraries
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import cv2
import uuid
import os
import numpy as np

# OpenGL initialization
window = init_glfw()
# Create the shader program
shader_program = Shader(vertex_shader_source, fragment_shader_source)
# Create the hand object
hand_color = [0.91, 0.75, 0.67] # skin color
hand_ = Hand(shader_program.get_program_number(), hand_color)



# Create the square object
square_color = [0.5, 0.5, 0.5]  # Gray color
square = Square(shader_program.get_program_number(), square_color)


# OpenCV initialization
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
cap = cv2.VideoCapture(0)

# Crear una instancia de la clase Background
background = Background(shader_program.get_program_number(), 800, 600, "texture.jpg")  # Ruta de la imagen de textura

# Habilitar el uso de texturas
glEnable(GL_TEXTURE_2D)



with mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5) as hands:
    while cap.isOpened() and not glfw.window_should_close(window):
        

        # Establecer el color de fondo
        glClearColor(0.53, 0.81, 0.92, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)
        # Clear the color buffer

        #background.draw()



        ret, frame = cap.read()
        # revert frame because it is mirrored
        frame = cv2.flip(frame, 1)

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = hands.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.multi_hand_landmarks:
            for num, hand in enumerate(results.multi_hand_landmarks):
                current_landmarks = []
                for idx, landmark in enumerate(hand.landmark):
                    coordinates = (landmark.x, landmark.y, landmark.z)
                    current_landmarks.append(coordinates)

                # convert the list to a numpy array
                current_landmarks = np.array(current_landmarks)
                # inverti los valores de y
                current_landmarks[:, 1] *= -1
                # convertir a coordenadas de OpenGL
                current_landmarks[:, 0] = (current_landmarks[:, 0] * 2) - 1
                current_landmarks[:, 1] = (current_landmarks[:, 1] * 2) + 1
                current_landmarks[:, 2] = (current_landmarks[:, 2] * 2) - 1
                
                print("current_landmarks:\n", current_landmarks, "\n")

                square_collided = False
                for landmark in current_landmarks:
                    if (
                        square.vertices[0, 0] <= landmark[0] <= square.vertices[2, 0] and
                        square.vertices[0, 1] <= landmark[1] <= square.vertices[2, 1]
                    ):
                        square_collided = True
                        break

                if square_collided:
                    square.move(hand_.movement)

                

                mp_drawing.draw_landmarks(image, hand, mp_hands.HAND_CONNECTIONS)

                hand_.change_all_coordinates(current_landmarks)
            # Draw the hand
            hand_.draw()
        # Draw the square
        square.draw()


        cv2.imshow('Hand Tracking', image)

        # Swap buffers
        glfw.swap_buffers(window)
        # Poll events
        glfw.poll_events()

        # Detener el bucle si se presiona la tecla 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


cap.release()
cv2.destroyAllWindows()


# Clean up resources
hand_.delete()
# Terminate GLFW
glfw.terminate()

