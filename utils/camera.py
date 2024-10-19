from enum import Enum

import glm


class Movement(Enum):
    FORWARD = 0
    BACKWARD = 1
    LEFT = 2
    RIGHT = 3


YAW = -90.0
PITCH = 0.0
SPEED = 300
SENSITIVITY = 0.05
ZOOM = 45.0


class Camera:
    def __init__(self, position=glm.vec3(0.0, 0.0, 0.0), up=glm.vec3(0.0, 1.0, 0.0), yaw=YAW, pitch=PITCH):
        self.Position = position
        self.Front = glm.vec3(0.0, 0.0, -1.0)
        self.Up = glm.vec3(0.0, 1.0, 0.0)
        self.Right = glm.vec3(0.0, 0.0, 0.0)
        self.WorldUp = up
        self.Yaw = yaw
        self.Pitch = pitch
        self.MovementSpeed = SPEED
        self.MouseSensitivity = SENSITIVITY
        self.Zoom = ZOOM

        self.update_camera_vectors()

    @classmethod
    def from_values(cls, pos_x, pos_y, pos_z, up_x, up_y, up_z, yaw, pitch):
        position = glm.vec3(pos_x, pos_y, pos_z)
        up = glm.vec3(up_x, up_y, up_z)
        return cls(position, up, yaw, pitch)

    def get_view_matrix(self):
        return glm.lookAt(self.Position, self.Position + self.Front, self.Up)

    def process_keyboard(self, direction, delta_time):
        velocity = self.MovementSpeed * delta_time
        if direction == Movement.FORWARD:
            self.Position += self.Front * velocity
        if direction == Movement.BACKWARD:
            self.Position -= self.Front * velocity
        if direction == Movement.LEFT:
            self.Position -= self.Right * velocity
        if direction == Movement.RIGHT:
            self.Position += self.Right * velocity

    def process_mouse_movement(self, x_offset, y_offset, constrain_pitch=True):
        x_offset *= self.MouseSensitivity
        y_offset *= self.MouseSensitivity

        self.Yaw += x_offset
        self.Pitch += y_offset

        if constrain_pitch:
            if self.Pitch > 89.0:
                self.Pitch = 89.0
            if self.Pitch < -89.0:
                self.Pitch = -89.0

        self.update_camera_vectors()

    def process_mouse_scroll(self, y_offset):
        self.Zoom -= y_offset
        if self.Zoom < 1.0:
            self.Zoom = 1.0
        if self.Zoom > 45.0:
            self.Zoom = 45.0

    def update_camera_vectors(self):
        front = glm.vec3(
            glm.cos(glm.radians(self.Yaw)) * glm.cos(glm.radians(self.Pitch)),
            glm.sin(glm.radians(self.Pitch)),
            glm.sin(glm.radians(self.Yaw)) * glm.cos(glm.radians(self.Pitch))
        )
        self.Front = glm.normalize(front)
        self.Right = glm.normalize(glm.cross(self.Front, self.WorldUp))
        self.Up = glm.normalize(glm.cross(self.Right, self.Front))
