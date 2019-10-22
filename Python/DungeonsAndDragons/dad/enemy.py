class enemy:
    def __init__ (self, apariencia):
        #dependiendo del numero es un enemigo u otro
        self.force = apariencia

        if apariencia==1:
            self.appearance= " "
            self.life= 3
        elif apariencia ==2:
            self.appearance= " "
            self.life= 5
        elif apariencia ==3:
            self.appearance= " "
            self.life= 10
        else:
            return False


    def get_appearance(self):
        return self.appearance

    def get_life(self):
        return self.live

    def set_(self, newLife):
        self.live= newLife

    def get_force(self):
        return self.force
