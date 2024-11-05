import glm 
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
from math import sin, cos, radians

class Camera(object): 
    def __init__(self, width, height):
        self.position = glm.vec3(0,0,0)
        #angulos de euler
        self.rotation = glm.vec3(0,0,0)
        #la camara no tiene escala
        self.screenWidth = width
        self.screenHeight = height
        self.usingLookAt = False
        
        self.CreateProjectionMatrix(60,0.1, 1000)

    def GetViewMatrix(self):
        
        if not self.usingLookAt:
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

            self.viewMatrix = glm.inverse(camMat)
            return self.viewMatrix
    
    def GetProjectionMatrix(self):
        return self.projectionMatrix

    def CreateProjectionMatrix(self, fov, nearPlane, farPlane):
        self.projectionMatrix = glm.perspective(glm.radians(fov), self.screenWidth/self.screenHeight, nearPlane, farPlane)

    def GetPosition(self):
        return self.position 
        
    def LookAt(self, center): #center el punto en el que nos vamos a estar enfocando
        self.usingLookAt = True
        viewMatrix = glm.lookAt(self.position, center, glm.vec3(0,1,0)) #glm.ve3 es el vector de arriba, el vector de arriba es el vector que se va a estar viendo en la pantalla
        
        # """
        # matrix
        # 1,0,0,0
        # 0,1,0,0
        # 0,0,1,0
        # 0,0,0,1
        
        # quaternion
        # x, y, z, w

        # """

        camMatrix = glm.inverse(viewMatrix)

        self.rotation = glm.degrees(glm.eulerAngles( glm.quat_cast(camMatrix) ) )  #nos da los angulos de euler

    def Orbit(self, center, distance, angleX, angleY): 
    
        self.position.x = center.x + sin(radians(angleX)) * cos(radians(angleY)) * distance
        self.position.y = center.y + sin(radians(angleY)) * distance
        self.position.z = center.z + cos(radians(angleX)) * cos(radians(angleY)) * distance
        self.LookAt(center)

        