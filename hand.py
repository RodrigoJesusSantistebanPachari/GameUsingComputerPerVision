from OpenGL.GL import *
from geometry import Line
import numpy as np

class Hand:
    def __init__(self, shader_program, color):
        self.shader_program = shader_program
        self.color = color
        self.lines = []
        self.movement = 0

        self.landmark_indices = [
            # Fingers
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 15, 16],
            [17, 18, 19, 20],
            # Thumb
            [1, 2, 3, 4],
            # Palm
            [1, 0, 5, 9, 13, 17, 0],
        ]

        # Define the vertices of the hand landmarks (example coordinates)
        self.landmarks = np.array([
            # Palm
            [0.0, -0.9, 0.0],
            # Thumb
            [-0.4, -0.6, 0.0],
            [-0.6, -0.2, 0.0],
            [-0.8, 0.0, 0.0],
            [-0.8, 0.2, 0.0],
            # Index
            [-0.4, 0.3, 0.0],
            [-0.5, 0.4, 0.0],
            [-0.5, 0.6, 0.0],
            [-0.6, 0.8, 0.0],
            # Middle
            [-0.13, 0.31, 0.0],
            [-0.15, 0.5, 0.0],
            [-0.17, 0.7, 0.0],
            [-0.19, 0.9, 0.0],
            # Ring
            [0.11, 0.24, 0.0],
            [0.2, 0.4, 0.0],
            [0.27, 0.6, 0.0],
            [0.35, 0.8, 0.0],
            # Pinky
            [0.33, 0.03, 0.0],
            [0.4, 0.2, 0.0],
            [0.5, 0.4, 0.0],
            [0.6, 0.6, 0.0],
        ], dtype=np.float32)

        print("self.landmarks.shape:\n", self.landmarks.shape, "\n")
        
        self.update()

    def update(self):
        self.delete()
        self.lines = []
        for indices in self.landmark_indices:
            self.set_data(indices)

    def set_data(self, indices):
        vertices = self.landmarks[indices]
        # print("vertices:\n", vertices, "\n")
        for i in range(len(vertices) - 1):
            self.lines.append(Line(vertices[i], vertices[i + 1], self.shader_program, self.color))

    def draw(self):
        for line in self.lines:
            line.draw()

    def change_all_coordinates(self, new_landmarks):
        temp = self.landmarks[0]
        self.landmarks = new_landmarks
        self.update()
        self.movement = self.landmarks[0] -temp


    def change_coordinates(self, index, new_coordinates):
        self.landmarks[index] = new_coordinates
        self.update()


    def move(self, time):
        # Define movement parameters
        movement_scale = 0.1  # Scale factor for movement
        movement_speed = 1.0  # Speed of movement

        # Copy the original hand landmark array
        modified_hand_landmarks = self.landmarks.copy()

        # Modify the coordinates randomly based on time and movement parameters
        # the los indices 0, 1, 5, 9, 13, 17 should not be modified
        
        random_change = (np.random.rand(21, 3) - 0.5) * movement_scale * np.sin(time * movement_speed)
        random_change[0] = np.zeros(3)
        random_change[1] = np.zeros(3)
        random_change[5] = np.zeros(3)
        random_change[9] = np.zeros(3)
        random_change[13] = np.zeros(3)
        random_change[17] = np.zeros(3)
        
        modified_hand_landmarks += random_change

        # Update the hand object
        self.change_all_coordinates(modified_hand_landmarks)


    def delete(self):
        for line in self.lines:
            line.delete()