'''
    Class gameProblem, implements simpleai.search.SearchProblem
'''


from simpleai.search import SearchProblem
# from simpleai.search import breadth_first,depth_first,astar,greedy
import simpleai.search


class GameProblem(SearchProblem):

    # Object attributes, can be accessed in the methods below

    MAP=None
    INITIAL_STATE= None
    GOAL = None
    CONFIG=None
    NUMCUSTOMERS= None
    MAXBAGS = 2 #de manera general se establece el maximo de cargas a 2
    COST= 0

    #MOVES = ('West','North','East','South','Cargar', 'Descargar') tupla con los movimientos

    INC = {'West': (-1,0), 'North': (0,-1), 'East': (1,0), 'South':(0,1)} #diccionario con los movimientos

   # --------------- Common functions to a SearchProblem -----------------

    def actions(self, state):
        '''Returns a LIST of the actions that may be executed in this state
        '''
        actions = []

        #se analizan los limites para no salirse en la busqueda
        maxLeft = 0
        maxRight = self.CONFIG['map_size'][0]-1
        maxUp = 0
        maxDown = self.CONFIG['map_size'][1]-1



        if state[0] in self.POSITIONS ['pizza']:
            actions.append("Cargar") #Si nos encontramos en la casilla de pizza cargamos la bolsa
        if (state[0] in state[3]) or (state[0] in state[4]) or (state[0] in state[5]):
            actions.append("Descargar") #Si estamos sobre un cliente 1, 2 o 3 y esta en la tupla de pedidos pendientes descargamos

        if state[0][0]> maxLeft and ((state[0][0]-1, state[0][1]) not in self.POSITIONS['building']):
            actions.append("West")
        if state[0][0]< maxRight and ((state[0][0]+1,state[0][1])not in self.POSITIONS['building']):
            actions.append("East")
        if state[0][1]> maxUp and ((state[0][0], state[0][1]-1) not in self.POSITIONS['building']):
            actions.append("North")
        if state[0][1]< maxDown and ((state[0][0],state[0][1]+1)not in self.POSITIONS['building']):
            actions.append("South")
        #Dependiendo de la casilla en la que se encuentre y el limite del mapa realiza una u otra accion

        return actions


    def result(self, state, action):
        '''Returns the state reached from this state when the given action is executed
        '''
        #print action #prueba para ver la accion realizada
        pos, c, p, t1, t2, t3= state #posicion, carga, pedidos, customer1, customer2, customer3
        #print state #prueba para comprobar el estado actual

        if action.count("Cargar"):
            if c<self.MAXBAGS and c<=p: #como mucho carga el maximo de la bolsa y no carga mas que los pedidos que tiene
                c +=1
        elif action.count("Descargar"):
            if c>0 and p> 0: #solo descarga si tiene pedidos y carga
                c-=1
                p-=1
                if state[0] in state[3]:
                    t1=list(t1) #pasa la tupla a lista para poder eliminar el elemento (x,y)
                    t1.remove(pos) #elimina el elemento
                    t1=tuple(t1) #lo vuelve a convertir en tupla

                if state[0] in state[4]:
                    #pasa los customer2 a la lista de customer1
                    t1=list(t1)
                    t2=list(t2)
                    t1.append(pos)
                    t2.remove(pos)
                    t1=tuple(t1)
                    t2=tuple(t2)
                if state[0] in state[5]:
                    #pasa los customer3 a la tupla de customer2
                    t2=list(t2)
                    t3=list(t3)
                    t2.append(pos)
                    t3.remove(pos)
                    t2=tuple(t2)
                    t3=tuple(t3)

        else:
            #dependiendo de la accion se modifica la posicion x e y
            pos=list(pos)
            pos[0] += self.INC[action][0]
            pos[1] += self.INC[action][1]
            pos=tuple(pos)

        new_state = (pos, c, p, t1,t2,t3)
        #print new_state #prueba para ver como quedaria el nuevo estado
        return new_state



    def is_goal(self, state):
        '''Returns true if state is the final state
        '''
        return state == self.GOAL

    def cost(self, state, action, state2):
        '''Returns the cost of applying `action` from `state` to `state2`.
           The returned value is a number (integer or floating point).
           By default this function returns `1`.
        '''
        self.COST= self.getAttribute(state[0],"cost")
        if self.MAXBAGS<3:
            #print "HOLAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA", self.COST #pruebas para ver como tiene en cuenta los costes
            return self.COST
        elif self.MAXBAGS<6:
            #print "HOLAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA", self.COST*2
            return self.COST*2
        elif self.MAXBAGS<9:
            #print "HOLAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA", self.COST*3
            return self.COST*3
        else:
            #print "HOLAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA", self.COST*4
            return self.COST*4



    def heuristic(self, state):
        '''Returns the heuristic for `state`
        '''
        return 1

    def setup (self):
        '''This method must create the initial state, final state (if desired) and specify the algorithm to be used.
           This values are later stored as globals that are used when calling the search algorithm.
           final state is optional because it is only used inside the is_goal() method

           It also must set the values of the object attributes that the methods need, as for example, self.SHOPS or self.MAXBAGS
        '''

        print '\nMAP: ', self.MAP, '\n'
    	print 'POSITIONS: ', self.POSITIONS, '\n'
        print 'CONFIG: ', self.CONFIG, '\n'

        #cuando la clave no esta en el diccionario la anadimos con una tupla vacia y asi evitar que de error
        if 'customer1' not in self.POSITIONS:
            self.POSITIONS['customer1']= ()
        if 'customer2' not in self.POSITIONS:
            self.POSITIONS['customer2']= ()
        if 'customer3' not in self.POSITIONS:
            self.POSITIONS['customer3']= ()

        self.NUMCUSTOMERS= (len(self.POSITIONS['customer1'])+len(self.POSITIONS['customer2'])*2+len(self.POSITIONS['customer3'])*3)
        #x, y, carga, numero de clientes, customers 1, customers 2, customers 3.
        initial_state= ((0,0),0,self.NUMCUSTOMERS, tuple(self.POSITIONS['customer1']), tuple(self.POSITIONS['customer2']),tuple(self.POSITIONS['customer3']))
        final_state= ((0,0),0,0,(),(),())


        #Algoritmos de busqueda a ejecutar
        #algorithm= simpleai.search.breadth_first
        #algorithm= simpleai.search.depth_first
        #algorithm= simpleai.search.uniform_cost
        #algorithm= simpleai.search.greedy
        algorithm= simpleai.search.astar
        return initial_state,final_state,algorithm


    def printState (self,state):
        '''Return a string to pretty-print the state '''
        pps=''
        return (pps)


    def getPendingRequests (self,state):
        ''' Return the number of pending requests in the given position (0-N).
            MUST return None if the position is not a customer.
            This information is used to show the proper customer image.
        '''
        if (state[0] in state[3]):
            return 1
        elif (state[0] in state[4]):
            return 2
        elif (state[0] in state[5]):
            return 3
        elif (state[0] in self.POSITIONS['customer1']) or (state[0] in self.POSITIONS['customer2']) or (state[0] in self.POSITIONS['customer3']) :
            return 0

    # -------------------------------------------------------------- #
    # --------------- DO NOT EDIT BELOW THIS LINE  ----------------- #
    # -------------------------------------------------------------- #

    def getAttribute (self, position, attributeName):
        '''Returns an attribute value for a given position of the map
           position is a tuple (x,y)
           attributeName is a string

           Returns:
               None if the attribute does not exist
               Value of the attribute otherwise
        '''
        tileAttributes=self.MAP[position[0]][position[1]][2]
        if attributeName in tileAttributes.keys():
            return tileAttributes[attributeName]
        else:
            return None

    def getStateData (self,state):
        stateData={}
        pendingItems=self.getPendingRequests(state)
        if pendingItems >= 0:
            stateData['newType']='customer{}'.format(pendingItems)
        return stateData

    # THIS INITIALIZATION FUNCTION HAS TO BE CALLED BEFORE THE SEARCH
    def initializeProblem(self,map,positions,conf,aiBaseName):
        self.MAP=map
        self.POSITIONS=positions
        self.CONFIG=conf
        self.AGENT_START = tuple(conf['agent']['start'])

        initial_state,final_state,algorithm = self.setup()
        if initial_state == False:
            print ('-- INITIALIZATION FAILED')
            return True

        self.INITIAL_STATE=initial_state
        self.GOAL=final_state
        self.ALGORITHM=algorithm
        super(GameProblem,self).__init__(self.INITIAL_STATE)

        print ('-- INITIALIZATION OK')
        return True

    # END initializeProblem
