from dad.map import map

import pygame#.sys
from pygame.locals import *
from random import randint

level=102
TamanioX, TamanioY= 800, 600 #tamanio del tablero

pygame.init ()
ventana = pygame.display.set_mode((TamanioX,TamanioY)) #mostrar ventana
pygame.display.set_caption("SNAKE") #Nombre de la ventana

#Cargar imagenes
green= pygame.image.load("images/green.png")
black= pygame.image.load("images/black.png")
red= pygame.image.load("images/red.png")


map = map (TamanioX, TamanioY, 0)
color= map.createMap()

#loop para el juego
while True:


    for i in color:
        if i ==0 :
            ventana.blit(red, i)

    #Cuando el usuario presiona la X superior derecha se termina el programa
    for evento in pygame.event.get():
        if evento.type== QUIT:
            pygame.quit()
            sys.exit()
    #Actualiza lo que esta pasando en la ventana
    pygame.display.update()
