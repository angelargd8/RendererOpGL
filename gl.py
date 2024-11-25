import glm 
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
from camera import Camera
from skybox import Skybox

class Renderer(object): 
    def __init__(self, screen):
        self.screen = screen
        _, _, self.width, self.height = screen.get_rect()
        
        # glClearColor(0.2, 0.2,0.2, 1)
        glClearColor(0, 0, 0, 1)
        glEnable(GL_DEPTH_TEST)
        # glEnable(GL_TEXTURE_2D)
        
        glViewport(0, 0, self.width, self.height)

        self.camera = Camera(self.width, self.height)
        self.time = 0
        self.lightIntensity = 0.1
        self.pointLight = glm.vec3(-10, 3, 0)
        
        self.scene = []
        self.skybox = None

        #skybox != environment map
        #skybox es una textura que se pone en el fondo
        #environment map es una textura que se pone en el objeto y son mas comunes para los models de iluminacion

    def CreateSkybox(self, textureList, vShader, fShader):
        self.skybox = Skybox(textureList, vShader, fShader)

    def FilledMode(self): 
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        
    def WireframeMode(self):
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    
    

    def Render(self): 
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        if self.skybox is not None:
            self.skybox.Render(self.camera.GetViewMatrix(), self.camera.GetProjectionMatrix())

        for obj in self.scene:
            #los atributos son por vertices, cuando llegan al pixel ya fueron interpolados para todos los pixeles en los triangulos
            #para los que son uniformes se manda el mismo valor al fragment shader y al vertex shader
            if obj.vShader is not None and obj.fShader is not None:
                shader_program = compileProgram(
                    compileShader(obj.vShader, GL_VERTEX_SHADER), 
                    compileShader(obj.fShader, GL_FRAGMENT_SHADER)
                )
                glUseProgram(shader_program)
                
                glUniform1f(glGetUniformLocation(shader_program, "time"), self.time)

                glUniform1f(glGetUniformLocation(shader_program, "lightIntensity"), self.lightIntensity)

                glUniformMatrix4fv(glGetUniformLocation(shader_program, "viewMatrix"), 1, GL_FALSE, glm.value_ptr(self.camera.GetViewMatrix()))

                glUniformMatrix4fv(glGetUniformLocation(shader_program, "projectionMatrix"), 1, GL_FALSE, glm.value_ptr(self.camera.GetProjectionMatrix()))

                glUniform3fv(glGetUniformLocation(shader_program, "pointLight"), 1, glm.value_ptr(self.pointLight))

                camera_position = self.camera.GetPosition()

                glUniform3fv(glGetUniformLocation(shader_program, "cameraPosition"), 1, glm.value_ptr(camera_position))

                glUniformMatrix4fv(glGetUniformLocation(shader_program, "modelMatrix"), 
                                        1, GL_FALSE, 
                                        glm.value_ptr(obj.GetModelMatrix())
                                        )
                
                obj.Render()