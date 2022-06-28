import pygame
from OpenGL.GL import glBindTexture, glTexParameteri, glTexImage2D, \
    GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_TEXTURE_WRAP_T, GL_REPEAT, \
    GL_TEXTURE_MIN_FILTER, GL_TEXTURE_MAG_FILTER, GL_LINEAR, GL_RGBA, \
    GL_UNSIGNED_BYTE, glGenTextures

class Texture:

    @staticmethod
    def load_texture(path:str, texture:glGenTextures):
        # Enlazar la textura
        glBindTexture(GL_TEXTURE_2D, texture)
        # Establecemos los parametros de envoltura de la textura 
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        # Establecemos los parametros de filtrado de la textura
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        # Cargamos la textura
        image = pygame.image.load(path)
        # Invertimos la imagen
        image = pygame.transform.flip(image, False, True)
        # Obtenemos las dimenciones de la imagen
        image_width, image_height = image.get_rect().size
        # Obtenemos los datos de la imagen
        image_data = pygame.image.tostring(image, "RGBA")
        # Especificamos la textura
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image_width, image_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)
        return texture