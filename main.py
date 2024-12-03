import glfw
import glm

from model.cube import Cube
from model.surface import Surface
from particles.cube_collider import CubeCollider
from particles.particle_system import *
from particles.plane_gen import PlaneParticleGenerator
from utils.camera import Camera, Movement
from utils.shader import Shader
from utils.texture import load_texture

# Конфигурация теней
SHADOW_WIDTH, SHADOW_HEIGHT = 1024, 1024

# Точки
BIRTH_SPEED = 4
POINTS_MAX_COUNT = 2000

# Камера
camera = Camera(glm.vec3(0.0, 1.0, 6.0))
lastX, lastY = 800 / 2.0, 600 / 2.0
firstMouse = True
deltaTime = 0.0
lastFrame = 0.0

# Модели
surface: Surface|None = None
cube: Cube | None = None
plane: Surface | None = None

# Текстуры
texture_grass_1 = None
texture_grass_4 = None

# Настройка света
lightPos = glm.vec3(-5.0, 4.0, -2.0)
lightSpeed = 0.5

# TODO("поворот эмиттера")
def get_rotation_matrix(mat4):
    return glm.rotate(mat4, glm.radians(45), glm.vec3(0.0, 0.0, -1.0))

# TODO("положение куба")
cube_pos = glm.vec3(3.0, 3.5, 0.0)

def setup_viewport(window):
    width, height = glfw.get_framebuffer_size(window)
    glViewport(0, 0, width, height)


def key_callback(window, key, _, action, __):
    global deltaTime, lightPos
    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window, True)
    if key == glfw.KEY_W:
        camera.process_keyboard(Movement.FORWARD, deltaTime)
    if key == glfw.KEY_S:
        camera.process_keyboard(Movement.BACKWARD, deltaTime)
    if key == glfw.KEY_A:
        camera.process_keyboard(Movement.LEFT, deltaTime)
    if key == glfw.KEY_D:
        camera.process_keyboard(Movement.RIGHT, deltaTime)
    if key == glfw.KEY_SPACE:
        camera.process_keyboard(Movement.UP, deltaTime)
    if key == glfw.KEY_LEFT_CONTROL:
        camera.process_keyboard(Movement.DOWN, deltaTime)

    if key == glfw.KEY_UP and action != glfw.RELEASE:
        lightPos.y += lightSpeed
    if key == glfw.KEY_DOWN and action != glfw.RELEASE:
        lightPos.y -= lightSpeed
    if key == glfw.KEY_LEFT and action != glfw.RELEASE:
        lightPos.x -= lightSpeed
    if key == glfw.KEY_RIGHT and action != glfw.RELEASE:
        lightPos.x += lightSpeed
    if key == glfw.KEY_PAGE_UP and action != glfw.RELEASE:
        lightPos.z += lightSpeed
    if key == glfw.KEY_PAGE_DOWN and action != glfw.RELEASE:
        lightPos.z -= lightSpeed


def scroll_callback(_, __, yoffset):
    camera.process_mouse_scroll(float(yoffset))


def cursor_position_callback(window, xpos, ypos):
    global firstMouse, lastX, lastY
    if glfw.get_mouse_button(window, glfw.MOUSE_BUTTON_LEFT) != glfw.PRESS:
        return
    if firstMouse:
        lastX, lastY = xpos, ypos
        firstMouse = False
    xoffset, yoffset = xpos - lastX, lastY - ypos
    lastX, lastY = xpos, ypos
    camera.process_mouse_movement(float(xoffset), float(yoffset))


def render_scene(shader):
    global texture_grass_1, texture_grass_4
    glActiveTexture(GL_TEXTURE0)
    # TODO("текстура для поверхности")
    glBindTexture(GL_TEXTURE_2D, texture_grass_1)

    shader.set_mat4("model", glm.mat4(1.0))
    shader.set_vec3("material.ambient", glm.vec3(0.6, 0.6, 0.6))
    shader.set_vec3("material.diffuse", glm.vec3(0.6, 0.6, 0.6))
    shader.set_vec3("material.specular", glm.vec3(0.5, 0.5, 0.5))
    shader.set_float("material.shininess", 128.0)
    surface.render()

    # TODO("текстура для фигур")
    glBindTexture(GL_TEXTURE_2D, texture_grass_4)

    # Создаем модельную матрицу для plane
    model_matrix = glm.mat4(1.0)
    model_matrix = glm.translate(model_matrix, glm.vec3(0.0, 1.0, 0.0))  # Смещение
    model_matrix = get_rotation_matrix(model_matrix)
    shader.set_mat4("model", model_matrix)
    plane.render()

    shader.set_mat4("model", glm.translate(glm.mat4(1.0), cube_pos))
    cube.render()


def main():
    global deltaTime, lastFrame, surface, texture_grass_1, texture_grass_4, cube, plane

    if not glfw.init():
        raise Exception("GLFW initialization failed")

    window = glfw.create_window(1600, 900, "Lab1", None, None)
    if not window:
        glfw.terminate()
        raise Exception("Failed to create GLFW window")

    glfw.make_context_current(window)
    setup_viewport(window)

    glfw.set_key_callback(window, key_callback)
    glfw.set_scroll_callback(window, scroll_callback)
    glfw.set_cursor_pos_callback(window, cursor_position_callback)
    glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)

    texture_grass_1 = load_texture("textures/Grass_01.png")
    texture_grass_4 = load_texture("textures/Grass_04.png")
    shader = Shader("shaders/shading.vert", "shaders/shading.frag")
    simple_depth_shader = Shader("shaders/depth.vert", "shaders/depth.frag")
    particle_shader = Shader("shaders/particle_shader.vert", "shaders/particle_shader.frag")
    depth_map_fbo = glGenFramebuffers(1)
    depth_map = glGenTextures(1)

    glBindTexture(GL_TEXTURE_2D, depth_map)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_DEPTH_COMPONENT, SHADOW_WIDTH, SHADOW_HEIGHT, 0, GL_DEPTH_COMPONENT, GL_FLOAT,
                 None)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_BORDER)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_BORDER)

    border_color = [1.0, 1.0, 1.0, 1.0]
    glTexParameterfv(GL_TEXTURE_2D, GL_TEXTURE_BORDER_COLOR, border_color)

    glBindFramebuffer(GL_FRAMEBUFFER, depth_map_fbo)
    glFramebufferTexture2D(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, GL_TEXTURE_2D, depth_map, 0)

    glDrawBuffer(GL_NONE)
    glReadBuffer(GL_NONE)

    glBindFramebuffer(GL_FRAMEBUFFER, 0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)

    shader.use()
    shader.set_int("diffuseTexture", 0)
    shader.set_int("shadowMap", depth_map_fbo)
    shader.set_vec3("lightColor", glm.vec3(0.6))

    shader.set_vec3("material.ambient", glm.vec3(0.6, 0.6, 0.6))
    shader.set_vec3("material.diffuse", glm.vec3(1.0, 0.5, 0.31))
    shader.set_vec3("material.specular", glm.vec3(0.5, 0.5, 0.5))
    shader.set_float("material.shininess", 64.0)

    surface = Surface(25)

    plane_size = 1
    plane = Surface(plane_size)
    cube = Cube(2)
    cube_collider = CubeCollider(cube_pos, cube)

    rotation_matrix = get_rotation_matrix(glm.mat4(1.0))
    point_particle_gen = PlaneParticleGenerator(glm.vec3(0.0, 1.0, 0.0), plane_size, plane_size, rotation_matrix)
    ps = ParticleSystem(particle_shader, POINTS_MAX_COUNT, point_particle_gen)

    def update_particle(particle, dt):
        cube_collider(particle, dt)
        if particle.pos.y <= 0.0 or particle.pos.y >= 8.0:
            particle.kill()

    while not glfw.window_should_close(window):
        current_frame = glfw.get_time()
        deltaTime = current_frame - lastFrame
        lastFrame = current_frame

        glClearColor(0.1, 0.1, 0.1, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        light_projection = glm.ortho(-10.0, 10.0, -10.0, 10.0, 1.0, 25.5)
        light_view = glm.lookAt(lightPos, glm.vec3(0.0), glm.vec3(0.0, 1.0, 0.0))
        light_space_matrix = light_projection * light_view

        shader.use()
        shader.set_vec3("lightPos", lightPos)
        shader.set_mat4("lightSpaceMatrix", light_space_matrix)

        simple_depth_shader.use()
        simple_depth_shader.set_mat4("lightSpaceMatrix", light_space_matrix)

        glViewport(0, 0, SHADOW_WIDTH, SHADOW_HEIGHT)
        glBindFramebuffer(GL_FRAMEBUFFER, depth_map_fbo)
        glClear(GL_DEPTH_BUFFER_BIT)

        glCullFace(GL_FRONT)
        render_scene(simple_depth_shader)
        glCullFace(GL_BACK)

        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        setup_viewport(window)

        shader.use()
        projection = glm.perspective(glm.radians(camera.Zoom), 1600 / 900, 0.1, 100.0)
        view = camera.get_view_matrix()
        shader.set_mat4("projection", projection)
        shader.set_mat4("view", view)

        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, depth_map)

        render_scene(shader)

        particle_shader.use()
        particle_shader.set_mat4("projection", projection)
        particle_shader.set_mat4("view", view)
        ps.update(deltaTime, BIRTH_SPEED, update_particle)
        ps.render()
        print(ps.alive_count())

        glFlush()
        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()


if __name__ == "__main__":
    main()
