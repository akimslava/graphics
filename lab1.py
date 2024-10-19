import math
from time import sleep

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

dimensions_count = 3

# Размеры
cylinder_height = 2.0

# Данные анимации
animating = False
object_movement_speed = 0.001
animation_speed_multiplier = 1.0
task_multiplier = 1.25

wire_teapot_animating = False
wire_teapot_pos = [-3, -1, 0]
wire_teapot_target_pos = [0, cylinder_height * (1 - 0.6), 0]

show_part_3 = False
cone_animating = False
cone_scale = 1.0
cone_target_scale = task_multiplier

cylinder_animating = False
cylinder_pos = [4, 0, 0]
cylinder_target_pos = [8, 0, 0]


# Параметры камеры
camera_pos = [0.0, 0.0, 10.0]
camera_front = [0.0, 0.0, -1.0]
camera_up = [0.0, 1.0, 0.0]
camera_speed = 0.01
yaw = -90.0
pitch = 0.0
window_width = 800
window_height = 600
first_mouse = True

keys = set()


def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glClearDepth(1.0)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)
    glShadeModel(GL_FLAT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, 1.0, 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)


def draw_cylinder():
    cylinder = gluNewQuadric()
    gluQuadricDrawStyle(cylinder, GLU_LINE)
    glRotatef(90, 1.0, 0.0, 0.0)
    gluCylinder(cylinder, 1.0, 1.0, cylinder_height, 32, 32)


def draw_cone():
    cone = gluNewQuadric()
    gluQuadricDrawStyle(cone, GLU_LINE)
    glRotatef(-90, 1.0, 0.0, 0.0)
    gluCylinder(cone, 1.0, 0.0, 2.0, 32, 32)


def process_input():
    global camera_pos
    global animating, animation_speed_multiplier

    right_vector = cross_product(camera_front, camera_up)

    if b'w' in keys or b's' in keys:
        direction_sign = 1 if b'w' in keys else -1
        camera_pos = list(map(
            lambda orig, front: orig + direction_sign * camera_speed * front,
            camera_pos, camera_front
        ))
    if b'a' in keys or b'd' in keys:
        direction_sign = 1 if b'd' in keys else -1
        camera_pos = list(map(
            lambda orig, right: orig + direction_sign * camera_speed * right,
            camera_pos, right_vector
        ))

    if b'+' in keys or b'-' in keys:
        direction_sign = 1 if b'+' in keys else -1
        animation_speed_multiplier += max(direction_sign * 0.2, 1 - animation_speed_multiplier)

    if b' ' in keys:
        animating = not animating


def cross_product(v1, v2):
    return [
        v1[1] * v2[2] - v1[2] * v2[1],
        v1[2] * v2[0] - v1[0] * v2[2],
        v1[0] * v2[1] - v1[1] * v2[0]
    ]


def normalize(v):
    length = math.sqrt(sum(map(lambda i: i ** 2, v)))
    return [v[i] / length for i in range(dimensions_count)]


def mouse_motion(x, y):
    global yaw, pitch, camera_front, first_mouse

    center_x = window_width // 2
    center_y = window_height // 2

    if first_mouse:
        glutWarpPointer(center_x, center_y)
        first_mouse = False
        return

    x_offset = x - center_x
    y_offset = center_y - y

    sensitivity = 0.1
    x_offset *= sensitivity
    y_offset *= sensitivity

    yaw += x_offset
    pitch += y_offset

    if pitch > 89.0:
        pitch = 89.0
    if pitch < -89.0:
        pitch = -89.0

    front = [
        math.cos(math.radians(yaw)) * math.cos(math.radians(pitch)),
        math.sin(math.radians(pitch)),
        math.sin(math.radians(yaw)) * math.cos(math.radians(pitch))
    ]
    camera_front = normalize(front)

    glutWarpPointer(center_x, center_y)


# pylint: disable-next=unused-argument
def keyboard_down(key, x, y):
    del x, y
    keys.add(key)


# pylint: disable-next=unused-argument
def keyboard_up(key, x, y):
    if key in keys:
        keys.remove(key)


def draw():
    global wire_teapot_pos
    global animating, animation_speed_multiplier
    global wire_teapot_animating
    global show_part_3, cone_animating, cone_scale, cone_target_scale
    global cylinder_animating, cylinder_pos, cylinder_target_pos

    process_input()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    camera_target = [camera_pos[i] + camera_front[i] for i in range(dimensions_count)]

    gluLookAt(*camera_pos + camera_target + camera_up)

    if animating:
        temp_wire_teapot_animating = False
        for ind in range(len(wire_teapot_target_pos)):
            if wire_teapot_pos[ind] < wire_teapot_target_pos[ind]:
                temp_wire_teapot_animating = True
                wire_teapot_pos[ind] += object_movement_speed * animation_speed_multiplier
        wire_teapot_animating = temp_wire_teapot_animating

        if not wire_teapot_animating:
            show_part_3 = True
            cone_animating = True

        if cone_animating:
            if cone_scale < cone_target_scale:
                cone_scale += 0.0002 * animation_speed_multiplier
            else:
                cone_animating = False
                cylinder_animating = True

        if cylinder_animating:
            for ind in range(len(cylinder_pos)):
                if cylinder_pos[ind] < cylinder_target_pos[ind]:
                    cylinder_pos[ind] += object_movement_speed * animation_speed_multiplier



    glPushMatrix()
    glTranslatef(0.0, 0.0, 0.0)
    draw_cylinder()
    glPopMatrix()

    glPushMatrix()
    glTranslatef(*wire_teapot_pos)
    glutWireTeapot(1.0)
    glPopMatrix()

    if show_part_3:
        glPushMatrix()
        glTranslatef(*cylinder_pos)
        draw_cylinder()
        glPopMatrix()

        glPushMatrix()
        glTranslatef(4.0, 0.0, 0.0)
        glScalef(cone_scale, cone_scale, cone_scale)
        draw_cone()
        glPopMatrix()

    sleep(0.001)
    glutSwapBuffers()
    glutPostRedisplay()


def main():
    global window_width, window_height
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(window_width, window_height)
    glutCreateWindow(b"OpenGL Wireframe Primitives")
    init()
    glutDisplayFunc(draw)
    glutKeyboardFunc(keyboard_down)
    glutKeyboardUpFunc(keyboard_up)
    glutPassiveMotionFunc(mouse_motion)
    glutMainLoop()


if __name__ == "__main__":
    main()
