#COLORES: RGB(rojo, verde, azul)

import pygame#.sys
from pygame.locals import *
from random import randint

level=102
TamanioX, TamanioY= 800, 600

pygame.init ()
ventana = pygame.display.set_mode((TamanioX,TamanioY))
pygame.display.set_caption("SNAKE") #Nombre de la ventana

#Cargar imagen
green= pygame.image.load("imagenSnake/green.png")
black= pygame.image.load("imagenSnake/black.png")
red= pygame.image.load("imagenSnake/red.png")


posX, posY= 15,15 #randint(0,TamanioX), randint(0, TamanioY)
posXR, posYR=15,15
SNAKE= [(posX, posY)]


velSnake= 50
movement= False
comido= True
lastAction= ""
tiempo= 0

#Funcion que crea posicion aleatoria para la casilla roja
def positionRed():
    #print ("HE ENTRADO A CREAR LA POSICION")
    posXR, posYR= randint(0,TamanioX-100), randint(0, TamanioY-100)
    centrado= False

    while centrado== False:
        if posXR-15>= 0 and ((posXR -15 )%100 ==0) and posXR<TamanioX:
            if posYR-15>= 0 and ((posYR -15 )%100 ==0)and posYR<TamanioY:
                centrado = True
            else:
                posYR+=1
        else:
            posXR +=1

    return posXR, posYR

#loop para el juego
while True:
    #print (tiempo, level)


    #Dependiendo del nivel va a una velocidad u a otra.
    if tiempo> level:
        if lastAction=='LEFT':
            posX-= velSnake
            if (posX, posY) not in SNAKE:
                SNAKE.append((posX,posY))
                del SNAKE [0:1]
            else:
                pygame.quit()
                sys.exit()
            if posX<0:
                pygame.quit()
                sys.exit()
                print ('GAME OVER')
        elif lastAction=='RIGHT':
            posX+= velSnake
            if (posX, posY) not in SNAKE:
                SNAKE.append((posX,posY))
                del SNAKE [0:1]
            else:
                pygame.quit()
                sys.exit()
            if posX>TamanioX:
                pygame.quit()
                sys.exit()
                print ('GAME OVER')
        elif lastAction== 'UP':
            posY-= velSnake
            if (posX, posY) not in SNAKE:
                SNAKE.append((posX,posY))
                del SNAKE [0:1]
            else:
                pygame.quit()
                sys.exit()
            if posY<0:
                pygame.quit()
                sys.exit()
                print ('GAME OVER')
        elif lastAction=='DOWN':
            posY +=velSnake
            if (posX, posY) not in SNAKE:
                SNAKE.append((posX,posY))
                del SNAKE [0:1]
            else:
                pygame.quit()
                sys.exit()
            if posY>TamanioY:
                pygame.quit()
                sys.exit()
                print ('GAME OVER')
        tiempo = 0

    #creacion del mapa (casillas verdes)
    for i in range(0,TamanioX/50):
        for j in range (0, TamanioY/50):
            ventana.blit(green, (i*50,j*50))

    ventana.blit(black, (posX, posY))

    #situacion del punto rojo en el mapa
    if comido== True:
        level-=2
        posXR, posYR = positionRed()
        #print (posXR, posYR)
        comido= False

    ventana.blit(red, (posXR, posYR))

    #Cuando el usuario presiona la X superior derecha se termina el programa
    for evento in pygame.event.get():
        if evento.type== QUIT:
            pygame.quit()
            sys.exit()

    #Mover imagen con el teclado
        elif evento.type == pygame.KEYDOWN:
            if evento.key== K_LEFT:
                if posX>15:
                    posX-= velSnake
                    tiempo =0
                    lastAction= 'LEFT'
                    if (posX, posY) not in SNAKE:
                        SNAKE.append((posX,posY))
                        del SNAKE [0:1]
                    else:
                        pygame.quit()
                        sys.exit()
            elif evento.key == K_RIGHT:
                if posX<(TamanioX-50):
                    posX+= velSnake
                    tiempo =0
                    lastAction= 'RIGHT'
                    if (posX, posY) not in SNAKE:
                        SNAKE.append((posX,posY))
                        del SNAKE [0:1]
                    else:
                        pygame.quit()
                        sys.exit()

            elif evento.key == K_UP:
                if posY>15:
                    posY-= velSnake
                    tiempo =0
                    lastAction= 'UP'
                    if (posX, posY) not in SNAKE:
                        SNAKE.append((posX,posY))
                        del SNAKE [0:1]
                    else:
                        pygame.quit()
                        sys.exit()
            elif evento.key == K_DOWN:
                if posY<(TamanioY-50):
                    posY+= velSnake
                    tiempo =0
                    lastAction= 'DOWN'
                    if (posX, posY) not in SNAKE:
                        SNAKE.append((posX,posY))
                        del SNAKE [0:1]
                    else:
                        pygame.quit()
                        sys.exit()

    #print ("Posicion negro:", posX, posY)
    #print ("Posicion rojo: ", posXR, posYR)

    #Si el rojo y el negro se encuentran en el mismo punto se come
    if posX == posXR and posY== posYR:
        comido = True
        SNAKE.append((posX,posY))

    #Imprime toda la lista de la serpiente
    for i in SNAKE:
        ventana.blit(black, i)
#        print ( i)
    tiempo +=1
    
    #Actualiza lo que esta pasando en la ventana
    pygame.display.update()
