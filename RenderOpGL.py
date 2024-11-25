import pygame
from pygame.locals import *
from gl import Renderer
from buffer import Buffer
from shaders import *
from model import Model
import glm
from camera import *

width = 540
height = 540

pygame.init()

screen = pygame.display.set_mode((width, height), pygame.OPENGL | pygame.DOUBLEBUF) #pygame.OPENGL Para dibujar pixles con open gl, # | pygame.DOUBLEBUF Para que no se vea el parpadeo  #| es un bitwise or
clock = pygame.time.Clock()
rend  = Renderer(screen)

skyboxTextures = ["textures/Forest/negx.jpg", 
                  "textures/Forest/posx.jpg", 
                  "textures/Forest/posy.jpg", 
                  "textures/Forest/negy.jpg", 
                  "textures/Forest/negz.jpg", 
                  "textures/Forest/posz.jpg"]  

rend.CreateSkybox(skyboxTextures, skybox_vertex_shader, skybox_fragment_shader)

def Models(stringModel, stringTexture, rotationY, rotationZ, rotationX, translationZ, translationY, translationX, scaleX, scaleY, scaleZ, vShader = None, fShader = None):
    model = Model(stringModel)
    model.AddTexture(stringTexture)
    rend.camera.position = glm.vec3(0,1,0)
    model.rotation.y = rotationY
    model.rotation.z = rotationZ    
    model.rotation.x = rotationX
    model.translation.z = translationZ
    model.translation.y = translationY
    model.translation.x = translationX
    model.scale.x = scaleX
    model.scale.y = scaleY
    model.scale.z = scaleZ

    model.vShader = vShader
    model.fShader = fShader

    return model

# rotacion y,z, x | traslacion z,y,x | escala x,y,z

gifts = "models/gifts/gifts.obj"
giftsTexture = "models/gifts/gifts.bmp"
giftsModel= Models(gifts, giftsTexture, 180, 180, 90, -5, 0, -4, 0.015, 0.015, 0.015, vertex_shader, fragment_shader)
rend.scene.append(giftsModel)

tree = "models/tree/tree.obj"
treeTexture = "models/tree/tree.bmp"
treeModel= Models(tree, treeTexture, 180, 180, 90, -5, 0, -1, 0.03, 0.03, 0.03, vertex_shader, fragment_shader)
rend.scene.append(treeModel)

reindeer = "models/reindeer/reindeer.obj"
reindeerTexture = "models/reindeer/reindeer.bmp"
reindeerModel= Models(reindeer, reindeerTexture, 180, 0, 90, -5, 0, 3, 0.015, 0.015, 0.015, vertex_shader, fragment_shader)
rend.scene.append(reindeerModel)
reindeerModel2= Models(reindeer, reindeerTexture, 180, 0, 90, -5, 0 , 2, 0.005, 0.008, 0.008, vertex_shader, fragment_shader)
rend.scene.append(reindeerModel2)

santa = "models/santa2/Santa.obj"
santaTexture = "models/santa2/Santa.bmp"
santaModel= Models(santa, santaTexture, 180, 180, 90, -5, 0, 3, 0.015, 0.015, 0.015, vertex_shader, fragment_shader)
rend.scene.append(santaModel)


isRunning = True
vShader  = vertex_shader
fShader  = fragment_shader

camDistance = 10 #esta es la que se manipula para el zoom in y out
camAngle = 0
camAngleY =40
camAngleX = 0

#limites
minCamAngleY = -55
maxCamAngleY = 55

minCamDistance = 1.8
maxCamDistance = 15


rend.SetShaders(vShader, fShader)

while isRunning: 
    deltaTime = clock.tick(60) / 1000.0
    keys = pygame.key.get_pressed() #teclas presionadas en este momento
    
    for event in pygame.event.get():
        if event.type == QUIT:
            isRunning = False
        #mover laa camara con el mouse
        elif event.type == pygame.MOUSEWHEEL:        
            if event.y <0 and camDistance < maxCamDistance:
                camDistance -= event.y * deltaTime * 10
            if event.y >0 and camDistance > minCamDistance:
                camDistance -= event.y * deltaTime * 10
            
        elif event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_ESCAPE:
                isRunning = False

            if event.key == pygame.K_SPACE:
                # rend.lightIntensity = 1.0 - rend.lightIntensity
                rend.WireframeMode()

            if event.key == pygame.K_1:
                rend.FilledMode()
                
            if event.key == pygame.K_2:
                #reset
                vShader = vertex_shader
                fShader = fragment_shader
                rend.SetShaders(vShader, fShader)
                
            if event.key == pygame.K_3:
                vShader = vertex_shader
                fShader = rainbow_shader
                rend.SetShaders(vShader, fShader)

            if event.key == pygame.K_4:
                #
                giftsModel.fShader = rainbow_shader
                treeModel.fShader = water_color_shader
                # giftsModel.SetShaders(giftsModel.vShader, giftsModel.fShader)
                # treeModel.SetShaders(treeModel.vShader, treeModel.fShader)
                # rend.SetShaders(giftsModel.vShader, giftsModel.fShader)
                # rend.SetShaders(treeModel.vShader, treeModel.fShader)

            if event.key == pygame.K_5:
                #
                vShader = water_shader
                fShader = water_color_shader
                rend.SetShaders(vShader, fShader)
                

            if event.key == pygame.K_6:
                #vShader = fat_shader
                # fShader = negative_shader
                vShader = rotate1_shader
                fShader = rainbow_shader
                rend.SetShaders(vShader, fShader)
                
            if event.key == pygame.K_7:
                vShader = close_shader
                rend.SetShaders(vShader, fShader)

            if event.key == pygame.K_8:
                fShader = radioactive_shader 
                rend.SetShaders(vShader, fShader)

            if event.key == pygame.K_9:
                fShader = distorsion_shader 
                rend.SetShaders(vShader, fShader)
               
            if event.key == pygame.K_0:
                treeModel.translation.z =-16
                vShader = rotate_shader 
                rend.SetShaders(vShader, fShader)
  
    if keys[K_LEFT]:
        rend.pointLight.x -= 10 * deltaTime
    
    if keys[K_RIGHT]:
        rend.pointLight.x += 10 * deltaTime

    if keys[K_UP]:
        rend.pointLight.z -= 10 * deltaTime
    
    if keys[K_DOWN]:
        rend.pointLight.x += 10 * deltaTime

    if keys[K_PAGEDOWN]:
        rend.pointLight.y -= 10 * deltaTime
        
    if keys[K_PAGEUP]:
        rend.pointLight.y += 10 * deltaTime

    if keys[K_a]:
        camAngleX -= 45 * deltaTime

    if keys[K_d]:
        camAngleX += 45 * deltaTime

    if keys[K_s]:
        camAngleY -= 45 * deltaTime
        camAngleY = max(minCamAngleY, min(camAngleY, maxCamAngleY)) 
    
    if keys[K_w]:
        camAngleY += 45 * deltaTime
        camAngleY = max(minCamAngleY, min(camAngleY, maxCamAngleY))     

    mouseButtons = pygame.mouse.get_pressed()
    #mover la camara con el mouse
    if mouseButtons[0]:
        rel = pygame.mouse.get_rel()
        camAngleX -= rel[0] * deltaTime * 5
        camAngleY -= rel[1] * deltaTime * 5

        if mouseButtons[1] > 0 and rend.camera.position.y < 2:
            rend.camera.position.y += rel[1] * rel[1] * deltaTime * 5

        if mouseButtons[1] <0  and rend.camera.position.y > -2:
            rend.camera.position.y += rel[1] * rel[1] * deltaTime * 5


    camDistance = max(minCamDistance, min(camDistance, maxCamDistance))
    camAngleY = max(minCamAngleY, min(camAngleY, maxCamAngleY))


    # rend.camera.LookAt(faceModel.translation)
    rend.camera.Orbit(treeModel.translation, camDistance, camAngleX, camAngleY)
    rend.time += deltaTime #delta time la acumulacion de los cuadros

    rend.Render()
    pygame.display.flip()
    

pygame.quit()

