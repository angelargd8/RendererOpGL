import glm 
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader


class Camera(object): 
    def __init__(self, width, height):
        self.position = glm.vec3(0,0,0)
        self.rotation = glm.vec3(0,0,0)
        #la camara no tiene escala
        self.screenWidth = width
        self.screenHeight = height
        
        self.CreateProjectionMatrix(60,0.1, 1000)

    def GetViewMatrix(self):
        # M = T * R * S
        # R = pitch * yaw * roll #rotar en pos: x, y,z
        identity = glm.mat4(1) #mtriz de identidad4*4y 1 en la diagonal
        #la matriz de identidad es de origen
        translateMat = glm.translate(identity, self.position) #matriz de traslacion, se traslada la matriz d eidentidad
        pitchMat = glm.rotate(identity, glm.radians(self.rotation.x), glm.vec3(1,0,0)) #se indic el angulo, luego el eje
        yawMat   = glm.rotate(identity, glm.radians(self.rotation.y), glm.vec3(0,1,0))
        rollMat  = glm.rotate(identity, glm.radians(self.rotation.z), glm.vec3(0,0,1))

        rotationMat = pitchMat * yawMat * rollMat
        camMat = translateMat * rotationMat
        return glm.inverse(camMat)
    
    def GetProjectionMatrix(self):
        return self.projectionMatrix

    def CreateProjectionMatrix(self, fov, nearPlane, farPlane):
        self.projectionMatrix = glm.perspective(glm.radians(fov), self.screenWidth/self.screenHeight, nearPlane, farPlane)

    def GetPosition(self):
        return self.position 
        
    # def LookAt(self, eye): #eyes se refuere al punto de destino, a donde quiero ver
    #     viewMatrix =glm.LookAt(eye, self.position, glm.vec3(0,1,0)) #regresa una matriz
    #     # # self.rotation = glm.eulerAngles(glm.quat_cast(viewMatrix))
    #     # self.rotation = glm.degrees(glm.euler_angles(glm.quat_cast(viewMatrix)))
    #     # #print(self.rotation)
        
