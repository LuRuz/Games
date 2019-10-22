from random import randint

class map:
    def __init__ (self, axisX, axisY, level):
        self.X= axisX
        self.Y= axisY
        self.level=level
        self.map= []

    def get_level(self):
        return self.level

    def set_level(self, newLevel):
        self.level= newLevel

    def createMap(self):
        #creamos el mapa negro completamente

        for i in range (0, self.X):
            for j in range (0, self.Y):
                self.map= 0

        #numSalas = randint (2, 6)
        #for i in range [0,numSalas]:

        return self.map []
