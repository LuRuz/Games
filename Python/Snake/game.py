#COLORES: RGB(rojo, verde, azul)

import pygame#.sys
from pygame.locals import *
from random import randint

Blanco= (255,255,255)
Rojo= (255, 0, 0)
Verde= (0, 255, 0)
Azul= (0,0, 255)
AzulMarino= (0, 0, 50)
Negro= (0,0,0)
Color2= pygame.Color(255, 120, 9)

TamanioX, TamanioY= 900, 700
numInvaders = randint(10, 50)
miFuente= miFuente
numLevel= miFuente.render("Prueba fuente", 0, (255,255,255))

pygame.init ()
ventana = pygame.display.set_mode((TamanioX,TamanioY))
pygame.display.set_caption("Space Invaders") #Nombre de la ventana

#Cargar imagen
spaceInvader= pygame.image.load("imagenes/spaceInvaders.png")
bulbasaur= pygame.image.load("imagenes/bulbasaur.png")
cohete= pygame.image.load("imagenes/cohete.png")

posX, posY= 100, 70 #randint(0,TamanioX), randint(0, TamanioY)
posXC, posYC= (int)(TamanioX/2), (TamanioY-100)
velocidad, velBulbasaur, velCohete = 2, 20, 5
movement= False

invadersPositions = []

posAux= [posX, posY]


for i in range(0, numInvaders):
    if posAux[0]< (TamanioX-60):
        invadersPositions= invadersPositions+ posAux
        posAux[0]+= 70
        #print ("HOLAAAA")
        #print (invadersPositions, numInvaders, posAux)
    else:
        posAux[0],posAux[1]=100, posAux[1]+100
        #print ("CHAOOOO")
        #print (invadersPositions, numInvaders)

print (invadersPositions, numInvaders)

def creationMap (color, posAuxX, posAuxY):
    #Colorear la ventana
    ventana.fill(color)
    #ventana.fill(Color2)

    #Incluye la imagen en la ventana siendo x e y la esquina superior izda
    for i in range(len(invadersPositions)):
        if i%2==0:
            posAuxX=invadersPositions[i]
        else:
            posAuxY=invadersPositions[i]
            ventana.blit(spaceInvader, (posAuxX,posAuxY))




#loop para el juego
while True:
    creationMap(AzulMarino, posX, posY)

    ventana.blit(bulbasaur, (posXC, posYC))
    #Cuando el usuario presiona la X superior derecha se termina el programa
    for evento in pygame.event.get():
        if evento.type== QUIT:
            pygame.quit()
            sys.exit()

    #Mover imagen con el teclado
        elif evento.type == pygame.KEYDOWN:
            if evento.key== K_LEFT:
                if posXC>10:
                    posXC-= velBulbasaur
            elif evento.key == K_RIGHT:
                if posXC<(TamanioX-100):
                    posXC+= velBulbasaur
            elif evento.key == K_UP:
                posXCo=posXC
                posYCo=posYC
                movement= True
            #elif evento.key == K_DOWN:
            #    posYC+= velocidad2

#mueve el objeto hacia la derecha e izquierda hasta que llega al final del tablero
    #print (posX, derecha, TamanioX)
    if movement == True:
        if posYCo>-100:
            ventana.blit(cohete, (posXCo, posYCo))
            posYCo-= velCohete
        else:
            movement=False


    #uso del cursor
    #posXC, posYC= pygame.mouse.get_pos()

    #Actualiza lo que esta pasando en la ventana
    pygame.display.update()
