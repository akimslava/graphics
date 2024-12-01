import OpenGL.GL as gl
from PIL import Image
import numpy as np


def load_texture(filename: str) -> int:
    texture_id = gl.glGenTextures(1)
    gl.glBindTexture(gl.GL_TEXTURE_2D, texture_id)

    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_REPEAT)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_REPEAT)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR_MIPMAP_LINEAR)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)

    image = Image.open(filename)
    image = image.transpose(Image.FLIP_TOP_BOTTOM)
    img_data = np.array(image)

    width, height = image.size
    nr_channels = img_data.shape[2] if len(img_data.shape) == 3 else 1

    if nr_channels == 1:
        format = gl.GL_RED
    elif nr_channels == 3:
        format = gl.GL_RGB
    elif nr_channels == 4:
        format = gl.GL_RGBA

    print(f"Loaded image with width = {width}, height = {height}, and format = {format}")

    gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, format, width, height, 0, format, gl.GL_UNSIGNED_BYTE, img_data)
    gl.glGenerateMipmap(gl.GL_TEXTURE_2D)

    return texture_id
