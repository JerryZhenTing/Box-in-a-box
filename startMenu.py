

from cmu_graphics import *
import random
import math
class destination:
    def __init__(self):
        self.width = 100
        self.height = 100
        self.size = 100
        self.locations = []
        
        
    def inBound(self,x,y): #check if the box moved to certain area
        coordinate = (x,y)
        for location in self.locations:
            if coordinate == location:
                return location
        return None
    
    def addLocation(self,location): #add location(tuple of x y value)into locations list
        x = location[0]
        y = location[1]
        coordinates = (x,y)
        self.locations.append(coordinates)
    
    def draw(self,canvasWidth,canvasHeight,colors,labels):
        for i in range (len(self.locations)):
            drawRect(self.locations[i][0], self.locations[i][1], self.width,self.height, fill = colors[i],border = 'black')
            drawLabel(labels[i], self.locations[i][0] +self.width//2 , self.locations[i][1] + self.height//2, bold = True)
    def selected(self,x,y):
        for i in range(len(self.locations)):
            if (x >= self.locations[i][0] and x <= self.locations[i][0] + self.size and 
                y >= self.locations[i][1] and y <= self.locations[i][1] + self.size):
                return i
        return None
    
def distance(x0,x1,y0,y1):
    return ((x0-x1)**2 + (y0-y1)**2)**0.5    
class block:
    def __init__(self,x,y,width,height,fill,opacity):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.fill = fill
        self.opacity = opacity
     
class backGroundBlocks:
    def __init__(self,x,y,dx,dy,color):
        self.size = 60
        self.keepSpawning = True
        self.x = x
        self.y = y
        self.color = color
        self.dx = dx
        self.dy = dy
    def spawnBlock(self):
        drawRect(self.x,self.y,self.size,self.size,fill = self.color, opacity = 50)
    def bounceHorizontally(self,width,height):
        self.x += self.dx
        if self.x >= width - self.size:
            self.x = width - self.size
            self.dx = -self.dx
        elif self.x <= 0:
            self.x = 0
            self.dx = -self.dx
    def bounceVertically(self,width,height):
        self.y += self.dy
        if self.y >= height - self.size:
            self.y = height - self.size 
            self.dy = -self.dy
        elif self.y <= 0:
            self.y = 0
            self.dy = -self.dy    
    

class board:
    def __init__(self,width,height,row,col):
        self.width = width
        self.height = height
        self.row = row
        self.col = col
    def drawBoard(self):
        for row in range(self.row):
            for col in range(self.col):
                self.drawCell(row, col)

    def drawBoardBorder(self):
    # draw the board outline (with double-thickness):
        drawRect(0, 0, self.width, self.height,
            fill=None, border='black',
            borderWidth=2)

    def drawCell(self,row, col):
        cellLeft, cellTop = self.getCellLeftTop(row, col)
        cellWidth, cellHeight = 60,60
        drawRect(cellLeft, cellTop, cellWidth, cellHeight,
                fill=None, border='black',
                borderWidth=2)

    def getCellLeftTop(self, row, col):
        cellWidth, cellHeight = 60, 60
        cellLeft = col * cellWidth
        cellTop = row * cellHeight
        return (cellLeft, cellTop)

    
    
    