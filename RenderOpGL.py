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

skyboxTextures = ["textures/skybox/right.jpg", 
                  "textures/skybox/left.jpg", 
                  "textures/skybox/top.jpg", 
                  "textures/skybox/bottom.jpg", 
                  "textures/skybox/front.jpg", 
                  "textures/skybox/back.jpg"]

rend.CreateSkybox(skyboxTextures, skybox_vertex_shader, skybox_fragment_shader)

faceModel =Model("models/model.obj")
faceModel.AddTexture("textures/model.bmp")
rend.camera.position = glm.vec3(0,2,0)

faceModel.rotation.y = 90
faceModel.translation.z =-10
# faceModel.translation.y = -2

faceModel.scale.x = 1
faceModel.scale.y = 1
faceModel.scale.z = 1


rend.scene.append(faceModel)

isRunning = True
vShader  = vertex_shader
fShader  = fragment_shader

camDistance = 5 #esta es la que se manipula para el zoom in y out
camAngle = 0

rend.SetShaders(vShader, fShader)


while isRunning: 
    deltaTime = clock.tick(60) / 1000.0
    keys = pygame.key.get_pressed() #teclas presionadas en este momento
    
    for event in pygame.event.get():
        if event.type == QUIT:
            isRunning = False
            
        elif event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_ESCAPE:
                isRunning = False
                
            if event.key == pygame.K_1:
                rend.FilledMode()
                
            if event.key == pygame.K_2:
                rend.WireframeMode()
                
            if event.key == pygame.K_3:
                vShader = vertex_shader
                rend.SetShaders(vShader, fShader)

            if event.key == pygame.K_4:
                fShader = fragment_shader
                rend.SetShaders(vShader, fShader)

            if event.key == pygame.K_5:
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
                faceModel.translation.z =-16
                vShader = rotate_shader 
                rend.SetShaders(vShader, fShader)
  
    if keys[K_LEFT]:
        # faceModel.rotation.y -= 10 * deltaTime #10 grados *seg
        rend.pointLight.x -= 1 * deltaTime
    
    if keys[K_RIGHT]:
        rend.pointLight.x += 1 * deltaTime

    if keys[K_UP]:
        # faceModel.rotation.y -= 10 * deltaTime #10 grados *seg
        rend.pointLight.z -= 1 * deltaTime
    
    if keys[K_DOWN]:
        rend.pointLight.x += 1 * deltaTime

    if keys[K_PAGEDOWN]:
        rend.pointLight.y -= 1 * deltaTime
        
    if keys[K_PAGEUP]:
        rend.pointLight.y += 1 * deltaTime

    if keys[K_a]:
        camAngle -= 45 * deltaTime

    if keys[K_d]:
        camAngle += 45 * deltaTime

    if keys[K_w]:
        camDistance -= 2 * deltaTime
    
    if keys[K_s]:
        camDistance += 2 * deltaTime
    
    # mouseButtons = pygame.mouse.get_pressed()

    # if mouseButtons[0]:
    #     camAngle += pygame.mouse.get_rel()[0] * deltaTime * 0.5



    # if keys[K_a]:
    #     rend.camera.position.x -= 1 * deltaTime
    
    # if keys[K_d]:
    #     rend.camera.position.x += 1 * deltaTime

    # if keys[K_w]:
    #     rend.camera.position.y += 1 * deltaTime

    # if keys[K_s]:
    #     rend.camera.position.y -= 1 * deltaTime #si no tuviera el delta time, se moveria una unidad

    rend.camera.LookAt(faceModel.translation)
    rend.camera.Orbit(faceModel.translation, camDistance, camAngle)
    rend.time += deltaTime #delta time la acumulacion de los cuadros

    rend.Render()
    pygame.display.flip()
    

pygame.quit()

