from cmu_graphics import *
from maze_generator import *
from startMenu import *
from player import *

import math
from math import isclose
import random 
#need to do:
#add push box
#finish things regarding scaling
#make bounds
#make first level
#make a maze generator (just generate a maze doesn't need to be functional)
#ratio of movement after becomes small is done, check push right playr movement
class recursiveBlock:
    def __init__(self,row,col):
        self.size = 60
        self.col = col
        self.row = row
        self.canvasSize = 900
        self.canBePushed = True #check if the recursive block can be pushed
        self.playerEntering = False
    def recurse(self,level,x,y,size):
        player = playerBox()
        if level == 0:
            drawRect(getRowCoordinate(y),getColCoordinate(x),size,size,fill = 'orange', border = 'orange')   
        else:
            recursiveBlock.recurse(self,level-1,1,1,self.canvasSize-100) #900 is canvas size
    
         
def getRowCoordinate(row):
   return row*60
def getColCoordinate(col):
   return col*60

def onAppStart(app):
    #canvas and background
    
    app.atMenu = True
    if app.atMenu:
        app.cellWidth = 60
        app.cellHeight = 60
    
    app.width = 900
    app.height = 900
    app.grid = board(app.width,app.height, 15,15)
    app.backGroundColor = 'skyBlue'
    app.choices = destination()
    app.center_X = 900//2
    app.center_Y = 900//2 
    app.choices.addLocation((app.center_X,app.center_Y))
    app.choices.addLocation((app.center_X,app.center_Y + 110))    
    app.choices.addLocation((app.center_X,app.center_Y + 220))
    app.colors = ['tan','sandyBrown','lightPink']
    app.labels = ['Maze Mode', 'level Selector', 'customize']  
    app.BackGroundBlockColors = ['royalBlue', 'mediumSlateBlue', 'aqua','forestGreen','yellow','lightCoral'] 
    app.blocks = []
    # app.block = backGroundBlocks(0,0,9,7,color)
    app.blockCount = 0
   #player
    app.player = playerBox()
    # if app.atMenu:
    #     app.playerY, app.playerX = getCenterCoordinate(app.playerRow,app.playerCol)    
    app.moveUp = False
    app.moveDown = False
    app.moveLeft = False
    app.moveRight = False
    app.CurrLocation = None
    app.counter = 0
    app.testPlayerShrink = False
    app.playerScaler = 1
    #recursive Block 
    app.recursiveBlock = recursiveBlock(5,5)
    app.recursiveBlockRow = 5
    app.recursiveBlockCol = 5
    app.scalingSpeed = 0
    app.recursiveBlockSize = 60
    app.scale = False
    app.scaler = 1
    app.level = 0
    app.ratio = 10 #ratio of after scaling and before scaling of recursive block
    app.recursiveBlockX, app.recursiveBlockY = getCenterCoordinate(app.recursiveBlockCol,app.recursiveBlockRow)
    app.middleBlockX,app.middleBlockY = app.recursiveBlockX,app.recursiveBlockY
    #maze mode
    app.mazeMode = False
    app.maze = generate_maze()
    app.timer = 0
    if app.mazeMode:
        app.playerRow = 0
        app.playerCol = 0
        app.playerY, app.playerX = getCenterCoordinateMazeMode(app.playerRow,app.playerCol)
        app.canMoveUp = True
        app.canMoveDown = True
        app.canMoveRight = True
        app.canMoveLeft = True
    #push box mode:
    app.pushBoxMode = False
    if app.pushBoxMode:
        app.playerRow, app.playerCol = 5,5
        app.playerY,app.playerX = getCenterCoordiante(app.playerRow,app.playerCol)
        app.playerTouching = False
        app.playerEntering = False
        app.playerLeaving = False
        app.moveCount = 0 #the amount of time movement key pressed if player and recursive block touching
        
def getCenterCoordinateMazeMode(row,col):
    return row*90+45,col*90+45
def getCenterCoordinate(row,col):
    return row*60+30, col*60+30
    
    
def redrawAll(app):
    #menu
    if app.atMenu:
        drawRect(0,0,app.width,app.height, fill = app.backGroundColor) 
        drawRect(200, 400,app.width-300, app.height-400, fill = 'mediumPurple', border = 'black') 
        for i in range(len(app.blocks)):
            app.blocks[i].spawnBlock()
        app.choices.draw(app.width,app.height,app.colors,app.labels)
    #recursive Block
    
        
    
    #mazeMode
    if app.mazeMode:
        [cell.draw() for cell in app.maze]
        #player box
        drawRect(app.playerX,app.playerY,90*app.playerScaler,90*app.playerScaler, align = 'center', fill = 'cyan')
        
    # if app.atMenu:
    #     drawRect(app.playerX,app.playerY,60*app.playerScaler,60*app.playerScaler, align = 'center')
    
    #push box mode
    if app.pushBoxMode:
        #backGround
        drawRect(0,0,900,900,fill = 'skyBlue')
        #recursive block
        col,row = getCenterCoordinate(app.recursiveBlockCol,app.recursiveBlockRow)
        drawRect(col,row,app.scaler*app.recursiveBlockSize,app.scaler*app.recursiveBlockSize, fill = 'orange',align = 'center')
        #blank block
        drawRect(col,row,app.scaler*(app.recursiveBlockSize-30),app.scaler*(app.recursiveBlockSize-30),fill =app.backGroundColor,align = 'center' )
        drawRect(col - 22.5*app.scaler,row,app.scaler*15,app.scaler*6,fill = 'green', align = 'center') 

        app.grid.drawBoard()
        #player
        drawRect(app.playerX,app.playerY,60*app.playerScaler,60*app.playerScaler,align = 'center', fill ='lightSalmon' )
def onStep(app):
    #draw background
    while len(app.blocks) <= 20:
        x = random.randint(0,app.width-30) #randomly spawn in blocks, 30 is the size of the background block
        y = random.randint(0,app.height-30)
        dx = random.randint(0,3)
        dy = random.randint(0,3) #speed of the block in y and x direction
        randomNum = random.randint(0,len(app.BackGroundBlockColors)-1)
        color = app.BackGroundBlockColors[randomNum]
        newBlock = backGroundBlocks(x,y,dx,dy,color)
        app.blocks.append(newBlock)
        app.blockCount += 1
    for i in range(len(app.blocks)):
        app.blocks[i].bounceVertically(app.width,app.height)
        app.blocks[i].bounceHorizontally(app.width,app.height)
    #finish drawing background
    #player movement animation
    if app.moveUp == True:
        app.counter += 5
        currLocation = app.currLocation[1]
        destination = currLocation - app.cellHeight
        if app.playerY == destination:
            app.moveUp = False
            app.counter = 0
        else:
            app.playerY -= 15
    elif app.moveDown == True: 
        currLocation = app.currLocation[1]
        destination = currLocation + app.cellHeight
        app.counter += 5
        if app.playerY == destination:
            app.moveDown = False
            app.counter = 0
        else:
            app.playerY += 15
        
    elif app.moveLeft == True: 
        app.counter += 5
        currLocation = app.currLocation[0]
        destination = currLocation - app.cellWidth
        if app.playerX == destination:
            app.moveLeft = False
            app.counter = 0
        else:
            app.playerX -= 15

    elif app.moveRight == True: 
        app.counter += 5
        currLocation = app.currLocation[0]
        destination = currLocation + app.cellHeight*app.playerScaler #manage the ratio after player becomes small
        
        if app.playerX == destination:
            app.moveRight = False
            app.counter = 0
        else:
            app.playerX += 15*app.playerScaler
            
    #recursive Block animation
    #scale up
    if app.scale == True:
        if app.scaler != app.ratio:
            # dist = distance(app.recursiveBlockX,app.topLeft[0],app.recursiveBlockY,app.topLeft[1])
            # app.scaler += app.scalingSpeed
            app.scaler += 3
            # print(app.scaler)     
            # if dist >= 0:
            #     app.recursiveBlockX -= 1
            #     app.recursiveBlockY -= 1    
            # print(app.scaler)
            app.playerX -= 60
        # else:
        #     app.scale = False
    #scale down
    if app.scale == True and app.playerLeaving:
        pass
    
    if app.testPlayerShrink == True:
        
        if not isclose(app.playerScaler, 0.1, abs_tol=1e-8):
            app.playerScaler -= 0.1
            app.playerX += 3.5
        else:
            app.testPlayerShrink = False
    #maze mode
    #reshape maze every 10 seconds
    if app.mazeMode:
        app.timer += 1
        if app.timer == 300:
            app.maze = generate_maze()
            app.timer = 0
# def onMousePress(app, mouseX, mouseY):
   
def onMousePress(app,mouseX,mouseY):
    selectedOption = app.choices.selected(mouseX,mouseY)
    if selectedOption != None:
        if selectedOption == 0:
            app.mazeMode = True
            app.atMenu = False
            app.playerY,app.playerX = getCenterCoordinateMazeMode(0,0)
            app.cellWidth, app.cellHeight = 90, 90
            app.playerRow,app.playerCol = 0,0
            app.timer = 0
        elif selectedOption == 1:
            app.mazeMode = False
            app.atMenu = False
            app.pushBoxMode = True
            app.playerTouching = False
            app.playerEntering = False
            app.playerLeaving = False 
            app.cellWidth, app.cellHeight = 60,60
            app.playerRow,app.playerCol = 2,2
            app.playerY,app.playerX = getCenterCoordinate(2,2)
            app.moveCount = 0
            
            
def canMove(cell):
    moveable = set()
    for key in cell.walls:
        if cell.walls[key] == False:
            moveable.add(key)
    return moveable
    
def onKeyPress(app, key): 
    #app.counter feature prevents spam clicking and currLocation from being updated every key press
    #so player block does not go out of range of the desired amount 
    #mazemode movement:
    if app.mazeMode: 
        find_index = lambda x,y: x + y*10 #10 is the amount of cols on maze board
        currentCell = app.maze[find_index(app.playerCol,app.playerRow)]
        moveableDirection = canMove(currentCell)
    
    
    if key == 'w' and app.counter == 0 and (app.mazeMode == False or 'top' in moveableDirection):
        app.currLocation = (app.playerX,app.playerY) 
        
        app.moveUp = True
        app.moveDown = False
        app.moveRight = False
        app.moveLeft = False
        # app.playerY -= app.cellHeight
        app.playerRow -= 1
        #checkLevel(app)
        
    elif key == 's' and app.counter == 0 and (app.mazeMode == False or 'bottom' in moveableDirection):
        app.currLocation = (app.playerX,app.playerY)
        app.moveDown = True
        app.moveUp = False
        app.moveLeft = False
        app.moveRight = False
        app.playerRow += 1
        #checkLevel(app)
    elif key == 'a' and app.counter == 0 and (app.mazeMode == False or 'left' in moveableDirection):
        app.currLocation = (app.playerX,app.playerY)
        app.moveLeft = True
        app.moveRight = False
        app.moveUp = False
        app.moveDown = False
        app.playerCol -= 1
        #checkLevel(app)
    elif key == 'd' and app.counter == 0 and (app.mazeMode == False or 'right' in moveableDirection):
        if app.recursiveBlockCol - app.playerCol == 1 and app.scale == False:
            app.playerTouching = True
        else:
            app.playerTouching = False    
        app.currLocation = (app.playerX,app.playerY)
        app.moveRight = True
        app.moveLeft = False
        app.moveUp = False
        app.moveDown = False
        app.playerCol += 1
        app.moveCount = 0
        
        if app.playerTouching:
            app.scale = True
            app.playerTouching = False
            app.moveRight = False
            app.playerCol -= 1
        
        #checkLevel(app)
    elif key == 'm':
        app.scale = True
    elif key == 'y':
        app.testPlayerShrink = True    
    # elif key == 't':
    #     app.mazeMode = not app.mazeMode
    #     if app.mazeMode:
    #         app.playerX,app.playerY = 0,0
    #     app.atMenu = not app.atMenu
def main():
   runApp()
main()