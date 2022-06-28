"""
    Proyecto Final de Graficación

    Autor: Rodriguez Venegas Angel de Jesus
"""
import pyrr
import math
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader

from texture import Texture
from obj import OBJ
from camera import Camera
from myShader import vertexLight_shader, fragmentLight_shader

class App:
    # Camara objeto
    cam = Camera()
    first_mouse = True

    def __init__(self, width:int=800, height:int=600):
        self.width = width
        self.height = height
        self.lastX, self.lastY = width / 2, height / 2
        # Inicializamos pygame
        pygame.init()
        # Configuración de la camera
        pygame.display.set_mode((self.width,self.height), pygame.DOUBLEBUF|pygame.OPENGL|pygame.RESIZABLE)
        pygame.display.set_caption("Proyecto Graficación")
        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)
        # Configuración de Backgroud y el modo del Display
        #glUseProgram(shader)
        glClearColor(0.1, 0.1, 0.1, 1)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)


    def mouse_look(self, xpos, ypos):
        if self.first_mouse:
            self.lastX = xpos
            self.lastY = ypos
            self.first_mouse = False

        xoffset = xpos - self.lastX
        yoffset = self.lastY - ypos

        self.lastX = xpos
        self.lastY = ypos

        self.cam.process_mouse_movement(xoffset, yoffset)

    def _models_loader(self):
        # Importamos nuestros modelos
        self.suelo_indices, self.suelo_buffer, self.suelo_vertex = OBJ.load_model("models/Suelo.obj")
        self.casa_piso_indices, self.casa_piso_buffer, self.casa_piso_vertex = OBJ.load_model("models/Casa_Piso.obj")
        self.casa_vidrio_indices, self.casa_vidrio_buffer, self.casa_vidrio_vertex = OBJ.load_model("models/Casa_Vidrio.obj")
        self.casa_cortina_indices, self.casa_cortina_buffer, self.casa_cortina_vertex = OBJ.load_model("models/Casa_Cortina.obj")
        self.casa_murof1_indices, self.casa_murof1_buffer, self.casa_murof1_vertex = OBJ.load_model("models/Casa_Muro_F1.obj", color=[1.0, 1.0, 1.0])
        self.casa_murof2_indices, self.casa_murof2_buffer, self.casa_murof2_vertex = OBJ.load_model("models/Casa_Muro_F2.obj", color=[1.0, 1.0, 1.0])
        self.casa_murob_indices, self.casa_murob_buffer, self.casa_murob_vertex = OBJ.load_model("models/Casa_Muro_B.obj", color=[1.0, 1.0, 1.0])
        self.casa_murol_indices, self.casa_murol_buffer, self.casa_murol_vertex = OBJ.load_model("models/Casa_Muro_L.obj", color=[1.0, 1.0, 1.0])
        self.casa_muror_indices, self.casa_muror_buffer, self.casa_muror_vertex = OBJ.load_model("models/Casa_Muro_R.obj", color=[1.0, 1.0, 1.0])
        self.casa_techo_indices, self.casa_techo_buffer, self.casa_techo_vertex = OBJ.load_model("models/Casa_Techo.obj", color=[1.0, 0.0, 0.0])
        self.casa_techo2_indices, self.casa_techo2_buffer, self.casa_techo2_vertex = OBJ.load_model("models/Casa_Techo2.obj", color=[1.0, 0.0, 0.0])

        self.casa_ventana_indices, self.casa_ventana_buffer, self.casa_ventana_vertex = OBJ.load_model("models/Casa_Ventana.obj", color=[1.0, 0.0, 0.0])
        self.casa_canaleta_indices, self.casa_canaleta_buffer, self.casa_canaleta_vertex = OBJ.load_model("models/Casa_Canaleta.obj", color=[1.0, 1.0, 1.0])
        self.casa_det1_indices, self.casa_det1_buffer, self.casa_det1_vertex = OBJ.load_model("models/Casa_Det1.obj", color=[1.0, 1.0, 1.0])
        self.casa_det2_indices, self.casa_det2_buffer, self.casa_det2_vertex = OBJ.load_model("models/Casa_Det2.obj", color=[1.0, 0.0, 0.0])
        self.casa_estructura_indices, self.casa_estructura_buffer, self.casa_estructura_vertex = OBJ.load_model("models/Casa_Estructura.obj", color=[0.683,0.706,0.734])
        
        self.puerta_indices, self.puerta_buffer, self.puerta_vertex = OBJ.load_model("models/Puerta.obj")
        
        # Creamos el shader
        self.shader = compileProgram(compileShader(vertexLight_shader, GL_VERTEX_SHADER), compileShader(fragmentLight_shader, GL_FRAGMENT_SHADER))
        # Creamos los buffers
        self.VAO = glGenVertexArrays(16)
        self.VBO = glGenBuffers(16)
        self.EBO = glGenBuffers(1)

        # Suelo VAO
        glBindVertexArray(self.VAO[0])
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO[0])
        glBufferData(GL_ARRAY_BUFFER, self.suelo_buffer.nbytes, self.suelo_buffer, GL_STATIC_DRAW)
        # Suelo Vertices
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, self.suelo_buffer.itemsize * 11, ctypes.c_void_p(0))
        # Suelo textures
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, self.suelo_buffer.itemsize * 11, ctypes.c_void_p(12))
        # Suelo normals
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, self.suelo_buffer.itemsize * 11, ctypes.c_void_p(20))
        glEnableVertexAttribArray(2)

        # Casa Piso VAO
        glBindVertexArray(self.VAO[1])
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO[1])
        glBufferData(GL_ARRAY_BUFFER, self.casa_piso_buffer.nbytes, self.casa_piso_buffer, GL_STATIC_DRAW)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, self.casa_piso_buffer.itemsize * 11, ctypes.c_void_p(0))
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, self.casa_piso_buffer.itemsize * 11, ctypes.c_void_p(12))
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, self.casa_piso_buffer.itemsize * 11, ctypes.c_void_p(20))
        glEnableVertexAttribArray(2)

        # Casa Vidrio VAO
        glBindVertexArray(self.VAO[2])
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO[2])
        glBufferData(GL_ARRAY_BUFFER, self.casa_vidrio_buffer.nbytes, self.casa_vidrio_buffer, GL_STATIC_DRAW)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, self.casa_vidrio_buffer.itemsize * 11, ctypes.c_void_p(0))
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, self.casa_vidrio_buffer.itemsize * 11, ctypes.c_void_p(12))
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, self.casa_vidrio_buffer.itemsize * 11, ctypes.c_void_p(20))
        glEnableVertexAttribArray(2)

        # Casa Cortina VAO
        glBindVertexArray(self.VAO[3])
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO[3])
        glBufferData(GL_ARRAY_BUFFER, self.casa_cortina_buffer.nbytes, self.casa_cortina_buffer, GL_STATIC_DRAW)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, self.casa_cortina_buffer.itemsize * 11, ctypes.c_void_p(0))
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, self.casa_cortina_buffer.itemsize * 11, ctypes.c_void_p(12))
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, self.casa_cortina_buffer.itemsize * 11, ctypes.c_void_p(20))
        glEnableVertexAttribArray(2)

        # Casa Muro Front 1 VAO
        glBindVertexArray(self.VAO[4])
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO[4])
        glBufferData(GL_ARRAY_BUFFER, self.casa_murof1_buffer.nbytes, self.casa_murof1_buffer, GL_STATIC_DRAW)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, self.casa_murof1_buffer.itemsize * 11, ctypes.c_void_p(0))
        glEnableVertexAttribArray(3)
        glVertexAttribPointer(3, 3, GL_FLOAT, GL_FALSE, self.casa_murof1_buffer.itemsize * 11, ctypes.c_void_p(32))
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, self.casa_murof1_buffer.itemsize * 11, ctypes.c_void_p(20))
        glEnableVertexAttribArray(2)

        # Casa Muro Front 2 VAO
        glBindVertexArray(self.VAO[5])
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO[5])
        glBufferData(GL_ARRAY_BUFFER, self.casa_murof2_buffer.nbytes, self.casa_murof2_buffer, GL_STATIC_DRAW)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, self.casa_murof2_buffer.itemsize * 11, ctypes.c_void_p(0))
        glEnableVertexAttribArray(3)
        glVertexAttribPointer(3, 3, GL_FLOAT, GL_FALSE, self.casa_murof2_buffer.itemsize * 11, ctypes.c_void_p(32))
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, self.casa_murof2_buffer.itemsize * 11, ctypes.c_void_p(20))
        glEnableVertexAttribArray(2)

        # Casa Muro Back VAO
        glBindVertexArray(self.VAO[6])
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO[6])
        glBufferData(GL_ARRAY_BUFFER, self.casa_murob_buffer.nbytes, self.casa_murob_buffer, GL_STATIC_DRAW)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, self.casa_murob_buffer.itemsize * 11, ctypes.c_void_p(0))
        glEnableVertexAttribArray(3)
        glVertexAttribPointer(3, 3, GL_FLOAT, GL_FALSE, self.casa_murob_buffer.itemsize * 11, ctypes.c_void_p(32))
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, self.casa_murob_buffer.itemsize * 11, ctypes.c_void_p(20))
        glEnableVertexAttribArray(2)

        # Casa Muro Letf VAO
        glBindVertexArray(self.VAO[7])
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO[7])
        glBufferData(GL_ARRAY_BUFFER, self.casa_murol_buffer.nbytes, self.casa_murol_buffer, GL_STATIC_DRAW)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, self.casa_murol_buffer.itemsize * 11, ctypes.c_void_p(0))
        glEnableVertexAttribArray(3)
        glVertexAttribPointer(3, 3, GL_FLOAT, GL_FALSE, self.casa_murol_buffer.itemsize * 11, ctypes.c_void_p(32))
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, self.casa_murol_buffer.itemsize * 11, ctypes.c_void_p(20))
        glEnableVertexAttribArray(2)

        # Casa Muro Right VAO
        glBindVertexArray(self.VAO[8])
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO[8])
        glBufferData(GL_ARRAY_BUFFER, self.casa_muror_buffer.nbytes, self.casa_muror_buffer, GL_STATIC_DRAW)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, self.casa_muror_buffer.itemsize * 11, ctypes.c_void_p(0))
        glEnableVertexAttribArray(3)
        glVertexAttribPointer(3, 3, GL_FLOAT, GL_FALSE, self.casa_muror_buffer.itemsize * 11, ctypes.c_void_p(32))
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, self.casa_muror_buffer.itemsize * 11, ctypes.c_void_p(20))
        glEnableVertexAttribArray(2)

        # Casa Techo VAO
        glBindVertexArray(self.VAO[9])
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO[9])
        glBufferData(GL_ARRAY_BUFFER, self.casa_techo_buffer.nbytes, self.casa_techo_buffer, GL_STATIC_DRAW)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, self.casa_techo_buffer.itemsize * 11, ctypes.c_void_p(0))
        glEnableVertexAttribArray(3)
        glVertexAttribPointer(3, 3, GL_FLOAT, GL_FALSE, self.casa_techo_buffer.itemsize * 11, ctypes.c_void_p(32))
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, self.casa_techo_buffer.itemsize * 11, ctypes.c_void_p(20))
        glEnableVertexAttribArray(2)

         # Casa Techo2 VAO
        glBindVertexArray(self.VAO[10])
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO[10])
        glBufferData(GL_ARRAY_BUFFER, self.casa_techo2_buffer.nbytes, self.casa_techo2_buffer, GL_STATIC_DRAW)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, self.casa_techo2_buffer.itemsize * 11, ctypes.c_void_p(0))
        glEnableVertexAttribArray(3)
        glVertexAttribPointer(3, 3, GL_FLOAT, GL_FALSE, self.casa_techo2_buffer.itemsize * 11, ctypes.c_void_p(32))
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, self.casa_techo2_buffer.itemsize * 11, ctypes.c_void_p(20))
        glEnableVertexAttribArray(2)
        
         # Casa Ventana VAO
        glBindVertexArray(self.VAO[11])
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO[11])
        glBufferData(GL_ARRAY_BUFFER, self.casa_ventana_buffer.nbytes, self.casa_ventana_buffer, GL_STATIC_DRAW)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, self.casa_ventana_buffer.itemsize * 11, ctypes.c_void_p(0))
        glEnableVertexAttribArray(3)
        glVertexAttribPointer(3, 3, GL_FLOAT, GL_FALSE, self.casa_ventana_buffer.itemsize * 11, ctypes.c_void_p(32))
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, self.casa_ventana_buffer.itemsize * 11, ctypes.c_void_p(20))
        glEnableVertexAttribArray(2)

         # Casa Canaleta VAO
        glBindVertexArray(self.VAO[12])
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO[12])
        glBufferData(GL_ARRAY_BUFFER, self.casa_canaleta_buffer.nbytes, self.casa_canaleta_buffer, GL_STATIC_DRAW)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, self.casa_canaleta_buffer.itemsize * 11, ctypes.c_void_p(0))
        glEnableVertexAttribArray(3)
        glVertexAttribPointer(3, 3, GL_FLOAT, GL_FALSE, self.casa_canaleta_buffer.itemsize * 11, ctypes.c_void_p(32))
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, self.casa_canaleta_buffer.itemsize * 11, ctypes.c_void_p(20))
        glEnableVertexAttribArray(2)

         # Casa Det1 VAO
        glBindVertexArray(self.VAO[13])
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO[13])
        glBufferData(GL_ARRAY_BUFFER, self.casa_det1_buffer.nbytes, self.casa_det1_buffer, GL_STATIC_DRAW)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, self.casa_det1_buffer.itemsize * 11, ctypes.c_void_p(0))
        glEnableVertexAttribArray(3)
        glVertexAttribPointer(3, 3, GL_FLOAT, GL_FALSE, self.casa_det1_buffer.itemsize * 11, ctypes.c_void_p(32))
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, self.casa_det1_buffer.itemsize * 11, ctypes.c_void_p(20))
        glEnableVertexAttribArray(2)

         # Casa Det2 VAO
        glBindVertexArray(self.VAO[14])
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO[14])
        glBufferData(GL_ARRAY_BUFFER, self.casa_det2_buffer.nbytes, self.casa_det2_buffer, GL_STATIC_DRAW)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, self.casa_det2_buffer.itemsize * 11, ctypes.c_void_p(0))
        glEnableVertexAttribArray(3)
        glVertexAttribPointer(3, 3, GL_FLOAT, GL_FALSE, self.casa_det2_buffer.itemsize * 11, ctypes.c_void_p(32))
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, self.casa_det2_buffer.itemsize * 11, ctypes.c_void_p(20))
        glEnableVertexAttribArray(2)

         # Casa Estructura VAO
        glBindVertexArray(self.VAO[15])
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO[15])
        glBufferData(GL_ARRAY_BUFFER, self.casa_estructura_buffer.nbytes, self.casa_estructura_buffer, GL_STATIC_DRAW)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, self.casa_estructura_buffer.itemsize * 11, ctypes.c_void_p(0))
        glEnableVertexAttribArray(3)
        glVertexAttribPointer(3, 3, GL_FLOAT, GL_FALSE, self.casa_estructura_buffer.itemsize * 11, ctypes.c_void_p(32))
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, self.casa_estructura_buffer.itemsize * 11, ctypes.c_void_p(20))
        glEnableVertexAttribArray(2)

    def _textures(self):
        #Generamos nombre de texturas
        self.textures = glGenTextures(4)
        Texture.load_texture("texturas/Suelo.jpg", self.textures[0])
        Texture.load_texture("texturas/Wood_Fence.jpg", self.textures[1])
        Texture.load_texture("texturas/Fencing_Mesh_Blue.png", self.textures[2])
        Texture.load_texture("texturas/Polished_Concrete_Old.jpg", self.textures[3])

        glClearColor(0.1, 0.1, 0.1, 1)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        glUseProgram(self.shader)
        self.projection = pyrr.matrix44.create_perspective_projection_matrix(45, self.width/self.height, 0.1, 100)
        self.suelo_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0, 0]))
        self.casa_piso_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0, 0]))
        self.casa_murof1_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0, 0]))
        self.casa_murof2_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0, 0]))
        self.casa_murob_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0, 0]))
        self.casa_murol_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0, 0]))
        self.casa_muror_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0, 0]))
        self.casa_techo_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0, 0]))
        self.casa_techo2_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0, 0]))

        self.casa_ventana_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0, 0]))
        self.casa_vidrio_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0, 0]))
        self.casa_canaleta_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0, 0]))
        self.casa_det1_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0, 0]))
        self.casa_det2_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0, 0]))
        self.casa_cortina_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0, 0]))
        self.casa_estructura_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0, 0]))
        
        self.model_loc = glGetUniformLocation(self.shader, "model")
        self.proj_loc = glGetUniformLocation(self.shader, "projection")
        self.view_loc = glGetUniformLocation(self.shader, "view")
        self.switcher_loc = glGetUniformLocation(self.shader, "switcher")
        self.light_loc = glGetUniformLocation(self.shader, "light")

        glUniformMatrix4fv(self.proj_loc, 1, GL_FALSE, self.projection)

    def draw(self):
        # Dibujamos elementos con textura
        glUniform1i(self.switcher_loc, 0)

        # Dibujamos el Suelo
        glBindVertexArray(self.VAO[0])
        glBindTexture(GL_TEXTURE_2D, self.textures[0])
        glUniformMatrix4fv(self.model_loc, 1, GL_FALSE, self.suelo_pos)
        glDrawArrays(GL_TRIANGLES, 0, len(self.suelo_indices))

        # Dibujamos la Casa Piso
        glBindVertexArray(self.VAO[1])
        glBindTexture(GL_TEXTURE_2D, self.textures[1])
        glUniformMatrix4fv(self.model_loc, 1, GL_FALSE, self.casa_piso_pos)
        glDrawArrays(GL_TRIANGLES, 0, len(self.casa_piso_indices))

        # Dibujamos la Casa Vidrio
        glBindVertexArray(self.VAO[2])
        glBindTexture(GL_TEXTURE_2D, self.textures[2])
        glUniformMatrix4fv(self.model_loc, 1, GL_FALSE, self.casa_vidrio_pos)
        glDrawArrays(GL_TRIANGLES, 0, len(self.casa_vidrio_indices))

        # Dibujamos la Casa Cortina
        glBindVertexArray(self.VAO[3])
        glBindTexture(GL_TEXTURE_2D, self.textures[3])
        glUniformMatrix4fv(self.model_loc, 1, GL_FALSE, self.casa_cortina_pos)
        glDrawArrays(GL_TRIANGLES, 0, len(self.casa_cortina_indices))

        # Dibujamos elementos con color ========================================
        glUniform1i(self.switcher_loc, 1)

        # Dibujamos la Casa Muro Front 1
        glBindVertexArray(self.VAO[4])
        glUniformMatrix4fv(self.model_loc, 1, GL_FALSE, self.casa_murof1_pos)
        glDrawArrays(GL_TRIANGLES, 0, len(self.casa_murof1_indices))
        # Dibujamos la Casa Muro Front 2
        glBindVertexArray(self.VAO[5])
        glUniformMatrix4fv(self.model_loc, 1, GL_FALSE, self.casa_murof2_pos)
        glDrawArrays(GL_TRIANGLES, 0, len(self.casa_murof2_indices))
        # Dibujamos la Casa Muro Back
        glBindVertexArray(self.VAO[6])
        glUniformMatrix4fv(self.model_loc, 1, GL_FALSE, self.casa_murob_pos)
        glDrawArrays(GL_TRIANGLES, 0, len(self.casa_murob_indices))
        # Dibujamos la Casa Muro Left
        glBindVertexArray(self.VAO[7])
        glUniformMatrix4fv(self.model_loc, 1, GL_FALSE, self.casa_murol_pos)
        glDrawArrays(GL_TRIANGLES, 0, len(self.casa_murol_indices))
        # Dibujamos la Casa Muro Ringht
        glBindVertexArray(self.VAO[8])
        glUniformMatrix4fv(self.model_loc, 1, GL_FALSE, self.casa_muror_pos)
        glDrawArrays(GL_TRIANGLES, 0, len(self.casa_muror_indices))
        # Dibujamos la Casa Techo
        glBindVertexArray(self.VAO[9])
        glUniformMatrix4fv(self.model_loc, 1, GL_FALSE, self.casa_techo_pos)
        glDrawArrays(GL_TRIANGLES, 0, len(self.casa_techo_indices))
        # Dibujamos la Casa Techo
        glBindVertexArray(self.VAO[10])
        glUniformMatrix4fv(self.model_loc, 1, GL_FALSE, self.casa_techo2_pos)
        glDrawArrays(GL_TRIANGLES, 0, len(self.casa_techo2_indices))
        # Dibujamos la Casa Ventana
        glBindVertexArray(self.VAO[11])
        glUniformMatrix4fv(self.model_loc, 1, GL_FALSE, self.casa_ventana_pos)
        glDrawArrays(GL_TRIANGLES, 0, len(self.casa_ventana_indices))
        # Dibujamos la Casa Canaleta
        glBindVertexArray(self.VAO[12])
        glUniformMatrix4fv(self.model_loc, 1, GL_FALSE, self.casa_canaleta_pos)
        glDrawArrays(GL_TRIANGLES, 0, len(self.casa_canaleta_indices))
        # Dibujamos la Casa Det1
        glBindVertexArray(self.VAO[13])
        glUniformMatrix4fv(self.model_loc, 1, GL_FALSE, self.casa_det1_pos)
        glDrawArrays(GL_TRIANGLES, 0, len(self.casa_det1_indices))
        # Dibujamos la Casa Det2
        glBindVertexArray(self.VAO[14])
        glUniformMatrix4fv(self.model_loc, 1, GL_FALSE, self.casa_det2_pos)
        glDrawArrays(GL_TRIANGLES, 0, len(self.casa_det2_indices))
        # Dibujamos la Casa Estructura
        glBindVertexArray(self.VAO[15])
        glUniformMatrix4fv(self.model_loc, 1, GL_FALSE, self.casa_estructura_pos)
        glDrawArrays(GL_TRIANGLES, 0, len(self.casa_estructura_indices))
        

    def isCollision(self,poss2:pyrr.Vector3, poss1:pyrr.Vector3):
        distance = math.sqrt(math.pow((poss2[0] - poss1[0]),2) + math.pow((poss2[1] - poss1[1]), 2) + math.pow((poss2[2] - poss1[2]), 2))
        if distance < 1:
            return True
        else:
            return False

    def collision(self):
        is_collision = False
        # Colicion con el suelo
        for i in range(0,len(self.casa_piso_vertex)): 
            aux = pyrr.Vector3([0.0,0.0,0.0])
            if i % 3 == 0: 
                start = i
                end = start + 3
                aux = pyrr.Vector3(self.casa_piso_vertex[start:end])
            if self.isCollision(aux, self.cam.camera_pos):
                is_collision = True
        
        # Colicion de Muros
        for i in range(0,len(self.casa_murof1_vertex)):
            aux = pyrr.Vector3([0.0,0.0,0.0])
            if i % 3 == 0: 
                start = i
                end = start + 3
                aux = pyrr.Vector3(self.casa_murof1_vertex[start:end])
            if self.isCollision(aux, self.cam.camera_pos):
                is_collision = True
        for i in range(0,len(self.casa_murof2_vertex)):
            aux = pyrr.Vector3([0.0,0.0,0.0])
            if i % 3 == 0: 
                start = i
                end = start + 3
                aux = pyrr.Vector3(self.casa_murof2_vertex[start:end])
            if self.isCollision(aux, self.cam.camera_pos):
                is_collision = True
        for i in range(0,len(self.casa_murob_vertex)):
            aux = pyrr.Vector3([0.0,0.0,0.0])
            if i % 3 == 0: 
                start = i
                end = start + 3
                aux = pyrr.Vector3(self.casa_murob_vertex[start:end])
            if self.isCollision(aux, self.cam.camera_pos):
                is_collision = True
        for i in range(0,len(self.casa_murol_vertex)):
            aux = pyrr.Vector3([0.0,0.0,0.0])
            if i % 3 == 0: 
                start = i
                end = start + 3
                aux = pyrr.Vector3(self.casa_murol_vertex[start:end])
            if self.isCollision(aux, self.cam.camera_pos):
                is_collision = True
        for i in range(0,len(self.casa_muror_vertex)):
            aux = pyrr.Vector3([0.0,0.0,0.0])
            if i % 3 == 0: 
                start = i
                end = start + 3
                aux = pyrr.Vector3(self.casa_muror_vertex[start:end])
            if self.isCollision(aux, self.cam.camera_pos):
                is_collision = True
        #Techo
        for i in range(0,len(self.casa_techo_vertex)):
            aux = pyrr.Vector3([0.0,0.0,0.0])
            if i % 3 == 0: 
                start = i
                end = start + 3
                aux = pyrr.Vector3(self.casa_techo_vertex[start:end])
            if self.isCollision(aux, self.cam.camera_pos):
                is_collision = True
        #Puerta
        for i in range(0,len(self.puerta_vertex)):
            aux = pyrr.Vector3([0.0,0.0,0.0])
            if i % 3 == 0: 
                start = i
                end = start + 3
                aux = pyrr.Vector3(self.puerta_vertex[start:end])
            if self.isCollision(aux, self.cam.camera_pos):
                is_collision = False

        return is_collision

    def run(self):
        self._models_loader()
        self._textures()
        # Bucle Principal
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False
                if event.type == pygame.VIDEORESIZE:
                    glViewport(0, 0, event.w, event.h)
                    self.projection = pyrr.matrix44.create_perspective_projection_matrix(45, event.w / event.h, 0.1, 100)
                    glUniformMatrix4fv(self.proj_loc, 1, GL_FALSE, self.projection)
            
            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[pygame.K_a]:
                self.cam.process_keyboard("LEFT", 0.08)
                if self.collision():
                    self.cam.process_keyboard("RIGHT", 0.08)
            if keys_pressed[pygame.K_d]:
                self.cam.process_keyboard("RIGHT", 0.08)
                if self.collision():
                    self.cam.process_keyboard("LEFT", 0.08)
            if keys_pressed[pygame.K_w]:
                self.cam.process_keyboard("FORWARD", 0.08)
                if self.collision():
                    self.cam.process_keyboard("BACKWARD", 0.08)
            if keys_pressed[pygame.K_s]:
                self.cam.process_keyboard("BACKWARD", 0.08)
                if self.collision():
                    self.cam.process_keyboard("FORWARD", 0.08)

            mouse_pos = pygame.mouse.get_pos()
            self.mouse_look(mouse_pos[0], mouse_pos[1])

            # Girar mouse 360 grados
            if mouse_pos[0] <= 0:
                pygame.mouse.set_pos((1279, mouse_pos[1]))
            elif mouse_pos[0] >= 1279:
                pygame.mouse.set_pos((0, mouse_pos[1]))
            
            # Limpia la pantalla para dibujar el siguiente cuadro
            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

            view = self.cam.get_view_matrix()
            glUniformMatrix4fv(self.view_loc, 1, GL_FALSE, view)

            ct = pygame.time.get_ticks() / 1000
            rot_x = pyrr.Matrix44.from_x_rotation(0.5 * ct)
            rot_y = pyrr.Matrix44.from_y_rotation(0.8 * ct)
            glUniformMatrix4fv(self.light_loc, 1, GL_FALSE, rot_x * rot_y)

            self.draw()

            pygame.display.flip()
            pygame.time.wait(15)
        pygame.quit()

if __name__ == "__main__":
    miApp = App(width=1280, height=720)
    miApp.run()