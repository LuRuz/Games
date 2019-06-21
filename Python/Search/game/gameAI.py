#! /usr/bin/env python
## Javier Huertas (2017-18)
## Alejandro Cervantes (2017-18)
## Based on code from:
## Daniel Borrajo (2016-17)
## To be used with python2.7
## Open source. Distributed as-is

import random
import time
import re

import os
import sys
import pygame


# IA code that performs simple searches for a solution
# We have to provide the state representation in this domain
# We have to provide the list of feasible actions in this domain
# We have to provide the search algorithm that stores the current solution
# We have to extract the action that corresponds to the next step
# We have to check that the provided state matches the expected state
from gameSearch import searchSolution, searchInfo

# Map loading, generation and handling
import maps

# Alumn configuration file for any given problem
sys.path.append(os.path.abspath("../student"))
import config
configuration = config.configuration

text_size = configuration['text_size']
tile_size = configuration['tile_size']

# Plan container
aiPlan=None   # Stores the plan
aiMapText="Now running" 

## Read events detects key presses in the keyboard.  
## Space = Pause execution
## S = Take an step in the plan
def readEvents(configuration, state):
    done=False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            continue
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                state['inPause'] = not state['inPause']
                state['step'] = False
                continue
            if event.key == pygame.K_s:
                state['step'] = True
                state['inPause'] = False
                continue
    return done, state

## Initialize the map and search for a viable solution to the problem
def initGame():
    # Read configuration
    global configuration
    random.seed(configuration['seed'])
    
    # Set images
    rawImages = dict()
    for tilekey, tiledict in configuration['maptiles'].iteritems():
        rawImages[tilekey]= tiledict['graphics']
    rawImages['agent']= configuration['agent']['graphics']
    
    # Get agent tile identifier
    aiBaseName = configuration['agent']['id']      
    
    # This must be consistent with the agent base locations
    state = {'prev_pos': configuration['agent']['start']}
    
    # State handlers for key events
    state['inPause']=False
    state['step']=False
    
    debugMap= configuration['debugMap']
   
    # Read or generate a random map
    if configuration['type'] == 'random':
        map = maps.createMap(configuration, state, configuration['debug'])
    else:
        map, configuration = maps.readMap(configuration)
        
    # Display the initial screen
    screen_size = [configuration['map_size'][0] * tile_size, configuration['map_size'][1] * tile_size + text_size]
    screen = pygame.display.set_mode(screen_size)
    
    def scale(f, d): return pygame.transform.scale(pygame.image.load(d[f]).convert(),(tile_size - 5, tile_size - 5))
    images = {tile: {t: scale(t,rawImages[tile]) for t in rawImages[tile]} for tile in rawImages}

    # Declare starting state
    state['prev_pos'] = configuration['agent']['start']
    
    # Save map if option is declared
    if configuration['save']:
        with open(configuration['file'], 'w') as f:
            f.write(maps.printableMap(map, configuration, False))

    # Print the initial map
    maps.printMap(map, configuration, images, screen, state, configuration['debug'],"Running search")
 
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    # --- In the IA201718 configuration we have planned in advance for the objective
    global aiPlan
    global aiMapText
    # Search for a solution to the problem
    aiPlan, problem, result, useViewer = searchSolution(map, configuration, state, aiBaseName, debugMap)
    
    # If a plan has been found, it is executed on the viewer
    if aiPlan:
        aiMapText = searchInfo(problem, result, useViewer)
        print ("----------------------- STARTING SEARCH ---------------------")
#        print("Retrieved a plan: {0}".format(aiPlan))
        state['searchOk']= True
        done= False
    else:
        aiMapText = "Search retrieved no plan for this problem"
        print("Search retrieved no plan for this problem")
        state['searchOk']=False

    return state, screen, images, map, configuration, clock

# Check if the final step of the plan has been reached
def checkFinish (state, configuration):
    return len(aiPlan)==0

# Calculate newPos, virtual movement to the next position of the agent
# Actual movement takes place in moveAgent
def planMoveAgent(actionName, mapa, state, configuration, newPos, tracep):
    def moveup (state, configuration, newPos):
        if state['prev_pos'][1] > 0:
            newPos[1] = newPos[1] - 1
        return newPos, state
            
    def moveright(state, configuration, newPos):
        if state['prev_pos'][0] < configuration['map_size'][0] - 1:
            newPos[0] = newPos[0] + 1
        return newPos, state
        
    def movedown(state, configuration, newPos):
        if state['prev_pos'][1] < configuration['map_size'][1] - 1:
            newPos[1] = newPos[1] + 1
        return newPos, state
    
    def moveleft(state, configuration, newPos):
        if state['prev_pos'][0] > 0:
            newPos[0] = newPos[0] - 1
        return newPos, state
    
    def stay(state, configuration, newPos):
        newPos= state['prev_pos']
        return newPos, state
    
    actionDefs = { 'North': moveup ,
                'East':  moveright,
                'South': movedown,
                'West':  moveleft,
                'default':  stay
              }
    
    if actionName in actionDefs.keys():
        f = actionDefs[actionName]
    else:
        f = actionDefs['default']
    
    return f(state, configuration, newPos)

# Update the state and manage collisions
# Calculations use the attributes of the map position
# Results are effects in the state and map, but may also reet newPos (colision), etc.
def moveAgent(state, mapa, newPos):
    
    def step (state, mapa ,newPos):
        old_pos = state['prev_pos']
        oldMapTileData=mapa[old_pos[0]][old_pos[1]]
        agentState = oldMapTileData[3]['agent']
        oldMapTileData[3]['agent'] = None
        oldMapTileData[3]['image'] = 'traversed'
        mapa[newPos[0]][newPos[1]][3]['agent'] = agentState
        return state, mapa, newPos

    return step(state,mapa,newPos)        

def changeAgentTileType (state,mapa,newTileType):
    '''
        This changes the map by updating the tile 'type' in the current position
    '''
    newPos=state['prev_pos']
    mapTileData=mapa[newPos[0]][newPos[1]]
    mapTileType=mapTileData[0]
    mapTileTypeList=configuration['maptiles']
    if newTileType in mapTileTypeList.keys():
#        print ('Getting image {} from file {}'.format(newType,mapTileGraphics[newImage]))
        print ('Setting position {},{} to type {}'.format(newPos[0],newPos[1],newTileType))
        mapa[newPos[0]][newPos[1]][0]=newTileType
    return state, mapa

def changeAgentTileImage (state,mapa,newImage):
    '''
        This changes the map by updating the tile 'image' in the current position
    '''
    newPos=state['prev_pos']
    mapTileData=mapa[newPos[0]][newPos[1]]
    mapTileType=mapTileData[0]
    mapTileGraphics=configuration['maptiles'][mapTileType]['graphics']
    if newImage in mapTileGraphics.keys():
        print ('Setting position {},{} to image {} from file {}'.format(newPos[0],newPos[1],newImage,mapTileGraphics[newImage]))
        mapTileData[3]['image']=newImage
    return state, mapa
    
# Main method
def main():
    global aiPlan # This variable stores the calculated solution
    global aiMapText # This variable stores a text obtained during the search

    pygame.init()
    cycle = 0
    
    # Initialize and calculate a plan
    state, screen, images, mapa, configuration, clock = initGame()
    # If initialization returned state = None, then we are done
    done = not state['searchOk']

    if configuration['debugMap']:
        print ("-------------- INITIAL MAP -------------")
        print (mapa)
    
    # -------- Main Game Loop -----------
    state['inPause']=True
    displayText= aiMapText
    
    while not done:
        # --- Main event loop
        cycle = cycle + 1
        done, state = readEvents(configuration, state)
        if done:
            continue
        
        newPos = list(state['prev_pos'])
        newImage = None
        newType = None

        # Game logic should go here

        # In this point we have planned in advance for the objective
        # The plan is stored in a global (aiPlan)
        
        if len(aiPlan)>0 and not state['inPause']:
            nextElement = aiPlan.pop(0) 
            nextAction = nextElement[0]
            newPos, state = planMoveAgent(nextAction, mapa, state, configuration, newPos, configuration['debug'])
            nextActionData = nextElement[1]; # This field is reserved for plan step attributes (NOT USED YET)
            displayText= aiMapText
            if 'showText' in nextActionData.keys():
                displayText=nextActionData['showText'] + '\n\n ----- SEARCH RESULTS ----- \n\n' + aiMapText
            if 'newImage' in nextActionData['onState'].keys():
                newImage=nextActionData['onState']['newImage']
            if 'newType' in nextActionData['onState'].keys():
                newType=nextActionData['onState']['newType']
            
        # Calculate the effects of the plan
        state, mapa, newPos = moveAgent(state,mapa,newPos)
        state['prev_pos'] = newPos
        if newImage:
            state,mapa = changeAgentTileImage(state,mapa,newImage)
        if newType:
            state,mapa = changeAgentTileType(state,mapa,newType)

        # Check end of simulation
        done = checkFinish(state, configuration)
    
        # Draw the new map
        maps.printMap(mapa, configuration, images, screen, state, configuration['debug'], show_text=displayText)
        
        # Limit to 60 frames per second
        clock.tick(60)
        time.sleep(configuration['delay'])
        if state['step']:
            state['inPause']=True
    
    if configuration['debugMap']:
        print ("-------------- FINAL MAP -------------")
        print (mapa)

    # Pause the simulation
    state['inPause']=True
    maps.printMap(mapa, configuration, images, screen, state, configuration['debug'], show_text=aiMapText)
    while state['inPause']:
        done, state = readEvents(configuration, state)

    # End pygame
    pygame.quit()

# Main execution
main()
