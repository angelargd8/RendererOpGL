import glm 
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
from camera import Camera

class Renderer(object): 
    def __init__(self, screen):
        self.screen = screen
        _,_ , self.width, self.height = screen.get_rect()
        
        glClearColor(0.2, 0.2,0.2, 1)

        glEnable(GL_DEPTH_TEST)
        glViewport(0,0, self.width, self.height)

        self.camera = Camera(self.width, self.height)
        self.time = 0
        self.value = 0

        self.pointLight = glm.vec3(0,0,0)
        
        self.scene= []
        self.active_shaders = None

    def FilledMode(self): 
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        
    def WireframeMode(self):
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

    def SetShaders(self, vShader, fShader):
        if vShader is not None and fShader is not None: 
            self.active_shaders = compileProgram( compileShader(vShader, GL_VERTEX_SHADER), 
                                                  compileShader(fShader, GL_FRAGMENT_SHADER)) #compileprogram va a esperar los shadrs a
        else: 
            self.active_shaders= None
            
    
    def Render(self): 
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        if self.active_shaders is not None: 
            glUseProgram(self.active_shaders) #los shaders activos en ese momento
            
            glUniform1f(glGetUniformLocation(self.active_shaders, "time") , self.time)
        
            glUniformMatrix4fv(glGetUniformLocation(self.active_shaders, "viewMatrix"), #ubicacion
                                          1, GL_FALSE, #matrices
                                          glm.value_ptr(self.camera.GetViewMatrix() )) #pointer

            glUniformMatrix4fv(glGetUniformLocation(self.active_shaders, "projectionMatrix"), #ubicacion
                                          1, GL_FALSE, #matrices
                                          glm.value_ptr(self.camera.GetProjectionMatrix() )) #pointer
            
            glUniform3fv(glGetUniformLocation(self.active_shaders, "pointLight"), 1, glm.value_ptr(self.pointLight))
            
            camera_position = self.camera.GetPosition()
            #glUniform3f(glGetUniformLocation(self.active_shaders, "cameraPosition"), camera_position.x, camera_position.y, camera_position.z)
            glUniform3fv(glGetUniformLocation(self.active_shaders, "cameraPosition"), 1, glm.value_ptr(camera_position))


        for obj in self.scene:
            #los atributos son por vertices, cuando llegan al pixel ya fueron interpolados para todos los pixeles en los triangulos
            #para los que son uniformes se manda el mismo valor al fragment shader y al vertex shader
            if self.active_shaders is not None: 
                glUniformMatrix4fv(glGetUniformLocation(self.active_shaders, "modelMatrix"), #ubicacion
                                          1, GL_FALSE, #matrices
                                          glm.value_ptr(obj.GetModelMatrix() ) #pointer
                                         )
            
                obj.Render()
    
