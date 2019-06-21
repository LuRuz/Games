'''n= int (input("Introduzca número elementos eje x: "))
m= int (input("Introduzca número elementos eje y: "))
tablero=[]
fila= []

for i in range (0,n):
    fila.append('X')

for i in range (0,m):
    tablero.append(fila)

for imprimir in tablero:
    print (imprimir)
'''

'''
n= int (input("Introduzca número elementos eje x: "))
m= int (input("Introduzca número elementos eje y: "))

print ("----------------------------")
for i in range (0, m):
    print ('X'*n)
'''

import sys

x='si'

while x=='si':
    tecla = sys.stdin.read(1)
    print ('Has presionado ', tecla)
    if tecla=='s':
        x='no'
