class character:
    def __init__ (self, nombre, nivel):
        self.name= nombre #no modificable
        self.appearance= "../images/red.png" #no modificable

        '''se pueden modificar '''
        self.life= 20
        self.force=1
        self.level= nivel

    def get_name(self):
        return self.name

    def get_appearance(self):
        return self.appearance


    def get_life(self):
        return self.live

    def set_(self, kill):
        self.live-= kill
        if self.live <=0:
            return False

    def get_force(self):
        return self.force

    def set_force(self, newForce):
        self.force=newForce
    
    def get_level(self):
        return self.level

    def set_level(self, newLevel):
        self.level= newLevel
