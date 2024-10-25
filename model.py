from obj import Obj
from buffer import Buffer
from pygame import image
import glm 
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader

class Model(object):
    def __init__(self,filename ):
        objFile = Obj(filename)
        self.vertices = objFile.vertices
        self.texCoords= objFile.texcoords
        self.normals = objFile.normals
        self.faces = objFile.faces
        self.texture= None
        
        self.buffer= Buffer(self.BuildBuffer())
        self.translation = glm.vec3(0,0,0)
        self.rotation= glm.vec3(0,0,0)
        self.scale = glm.vec3(1,1,1)
     
    def GetModelMatrix(self):
        # M = T * R * S
        # R = pitch * yaw * roll #rotar en pos: x, y,z
        identity = glm.mat4(1) #mtriz de identidad4*4y 1 en la diagonal
        #la matriz de identidad es de origen
        translateMat = glm.translate(identity, self.translation) #matriz de traslacion, se traslada la matriz d eidentidad
        pitchMat = glm.rotate(identity, glm.radians(self.rotation.x), glm.vec3(1,0,0)) #se indic el angulo, luego el eje
        yawMat   = glm.rotate(identity, glm.radians(self.rotation.y), glm.vec3(0,1,0))
        rollMat  = glm.rotate(identity, glm.radians(self.rotation.z), glm.vec3(0,0,1))

        rotationMat = pitchMat * yawMat * rollMat
        
        scaleMat = glm.scale(identity, self.scale)
        
        return translateMat * rotationMat * scaleMat
        
        
    def BuildBuffer(self):
        data = []
        
        for face in self.faces: 
            faceVerts = []
            
            for i in range(len(face)): #porque unas caras tienen 3 vertices y otras 4  #si  hay 4 vertices, hay que hacer otro tringulo
                vert = []
               
                position = self.vertices[face[i][0] -1] #-1 porque las caras empiezan en 1
                
                for value in position:
                    vert.append(value)
                    
                vts = self.texCoords[face[i][1] -1]
                
                for value in vts:
                    vert.append(value)
                    
                normals= self.normals[face[i][2] -1]
                
                for value in normals: 
                    vert.append(value)
                    
                #luego de agregar los values se ponen en el vertice
                faceVerts.append(vert)
                
            #construye un triangulo
            for value in faceVerts[0]: data.append(value)
            for value in faceVerts[1]: data.append(value)
            for value in faceVerts[2]: data.append(value)
            
            #el segundo triangulo
            if (len(faceVerts) == 4):
                for value in faceVerts[0]: data.append(value)
                for value in faceVerts[2]: data.append(value)
                for value in faceVerts[3]: data.append(value)
                
        return data 
    
    def AddTexture(self, textureFilename):
        self.textureSurface = image.load(textureFilename)
        self.textureData = image.tostring(self.textureSurface, "RGB", True) #rgb formato y pregunta si esta volteado 
        self.texture = glGenTextures(1)
        
        
    def Render(self):
              
        #dar la textura
        if self.texture is not None:
            
            glActiveTexture(GL_TEXTURE0) #activar la textura 0
            glBindTexture(GL_TEXTURE_2D, self.texture) #eleccionar la textura, se dice cual
        
            glTexImage2D(GL_TEXTURE_2D,                           # texture type
                         0,                                       # positions
                         GL_RGB,                                  # format
                         self.textureSurface.get_width(),         # width
                         self.textureSurface.get_height(),        # height
                         0,                                       # border
                         GL_RGB,                                  # format
                         GL_UNSIGNED_BYTE,                        # type, unsigned, solo positivos
                         self.textureData)                        # data, los datos d ela textur
            #mejorar las texturas
            glGenerateMipmap(GL_TEXTURE_2D)

        self.buffer.Render()

                                  

