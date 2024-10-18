import glfw
import glm
from OpenGL.GL import *

from model.cone import Cone
from model.cylinder import Cylinder
from model.surface import Surface
from model.teapot import Teapot
from utils.camera import Camera, Movement
from utils.shader import Shader
from utils.texture import load_texture

SHADOW_WIDTH, SHADOW_HEIGHT = 1024, 1024

camera = Camera(glm.vec3(0.0, 1.0, 6.0))
lastX, lastY = 800 / 2.0, 600 / 2.0
firstMouse = True
deltaTime = 0.0
lastFrame = 0.0

surface: Surface
cylinder: Cylinder
teapot: Teapot
cone: Cone

textureID: int
cylinder_textureID: int

lightPos = glm.vec3(-5.0, 4.0, -2.0)
lightSpeed = 0.5


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


def scroll_callback(_, __, y_offset):
    camera.process_mouse_scroll(float(y_offset))


def cursor_position_callback(_, xpos, y_pos):
    global firstMouse, lastX, lastY
    if firstMouse:
        lastX, lastY = xpos, y_pos
        firstMouse = False
    x_offset, y_offset = xpos - lastX, lastY - y_pos
    lastX, lastY = xpos, y_pos
    camera.process_mouse_movement(float(x_offset), float(y_offset))


def render_scene(shader):
    glActiveTexture(GL_TEXTURE0)
    glBindTexture(GL_TEXTURE_2D, textureID)

    model = glm.mat4(1.0)
    shader.set_mat4("model", model)
    shader.set_vec3("material.ambient", glm.vec3(0.6, 0.6, 0.6))
    shader.set_vec3("material.diffuse", glm.vec3(0.6, 0.6, 0.6))
    shader.set_vec3("material.specular", glm.vec3(0.5, 0.5, 0.5))
    shader.set_float("material.shininess", 128.0)
    surface.render()

    glBindTexture(GL_TEXTURE_2D, cylinder_textureID)
    model = glm.mat4(1.0)
    shader.set_mat4("model", model)
    shader.set_vec3("material.ambient", glm.vec3(0.6, 0.6, 0.6))
    shader.set_vec3("material.diffuse", glm.vec3(0.6, 0.6, 0.6))
    shader.set_vec3("material.specular", glm.vec3(0.5, 0.5, 0.5))
    shader.set_float("material.shininess", 64.0)
    cylinder.render()

    model = glm.translate(glm.mat4(1.0), glm.vec3(3.0, 1.0, 0.0))
    model = glm.scale(model, glm.vec3(0.1))
    shader.set_mat4("model", model)
    shader.set_vec3("material.ambient", glm.vec3(0.5, 0.5, 0.5))
    shader.set_vec3("material.diffuse", glm.vec3(0.7, 0.7, 0.7))
    shader.set_vec3("material.specular", glm.vec3(1.0, 1.0, 1.0))
    shader.set_float("material.shininess", 128.0)
    teapot.render()

    model = glm.translate(glm.mat4(1.0), glm.vec3(-3.0, 0.0, 0.0))
    shader.set_mat4("model", model)
    shader.set_vec3("material.ambient", glm.vec3(0.3, 0.3, 0.3))
    shader.set_vec3("material.diffuse", glm.vec3(0.8, 0.8, 0.8))
    shader.set_vec3("material.specular", glm.vec3(0.0, 0.0, 0.0))
    shader.set_float("material.shininess", 1.0)
    cone.render()


def main():
    global deltaTime, lastFrame, surface, cylinder, teapot, cone, textureID, cylinder_textureID

    if not glfw.init():
        raise Exception("GLFW initialization failed")

    window = glfw.create_window(1600, 1440, "Lab1", None, None)
    if not window:
        glfw.terminate()
        raise Exception("Failed to create GLFW window")

    glfw.make_context_current(window)
    setup_viewport(window)

    glfw.set_key_callback(window, key_callback)
    glfw.set_scroll_callback(window, scroll_callback)
    glfw.set_cursor_pos_callback(window, cursor_position_callback)
    glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)

    textureID = load_texture("textures/Grass_04.png")
    cylinder_textureID = load_texture("textures/Grass_01.png")
    shader = Shader("shaders/shading.vert", "shaders/shading.frag")
    simple_depth_shader = Shader("shaders/depth.vert", "shaders/depth.frag")
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

    shader.use()
    shader.set_int("diffuseTexture", 0)
    shader.set_int("shadowMap", depth_map_fbo)
    shader.set_vec3("lightColor", glm.vec3(0.6))

    shader.set_vec3("material.ambient", glm.vec3(0.6, 0.6, 0.6))
    shader.set_vec3("material.diffuse", glm.vec3(1.0, 0.5, 0.31))
    shader.set_vec3("material.specular", glm.vec3(0.5, 0.5, 0.5))
    shader.set_float("material.shininess", 64.0)

    surface = Surface()
    cylinder = Cylinder(1.0, 1.5)
    teapot = Teapot("obj/teapot.obj")
    cone = Cone(1.0, 1.5)

    while not glfw.window_should_close(window):
        current_frame = glfw.get_time()
        deltaTime = current_frame - lastFrame
        lastFrame = current_frame

        glClearColor(0.1, 0.1, 0.1, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        light_projection = glm.ortho(-10.0, 10.0, -10.0, 10.0, 1.0, 25.5)
        light_view = glm.lookAt(lightPos, glm.vec3(0.0), glm.vec3(0.0, 1.0, 0.0))
        light_space_matrix = light_projection * light_view

        shader.set_vec3("lightPos", lightPos)
        shader.set_mat4("lightSpaceMatrix", light_space_matrix)

        simple_depth_shader.use()
        simple_depth_shader.set_mat4("lightSpaceMatrix", light_space_matrix)

        glViewport(0, 0, SHADOW_WIDTH, SHADOW_HEIGHT)
        glBindFramebuffer(GL_FRAMEBUFFER, depth_map_fbo)
        glClear(GL_DEPTH_BUFFER_BIT)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, textureID)

        glCullFace(GL_FRONT)
        render_scene(simple_depth_shader)
        glCullFace(GL_BACK)

        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        setup_viewport(window)

        shader.use()
        projection = glm.perspective(glm.radians(camera.Zoom), 800 / 600, 0.1, 100.0)
        view = camera.get_view_matrix()
        shader.set_mat4("projection", projection)
        shader.set_mat4("view", view)

        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, depth_map)

        render_scene(shader)

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()


if __name__ == "__main__":
    main()
