from cmu_graphics import *
from random import choice
TILE = 60 
cols, rows = 600//TILE, 600// TILE

class Cell:
    def __init__(self,x,y):
        self.x,self.y = x,y
        self.walls = {'top':True,'right':True,'bottom':True,'left':True}
        self.visited = False
    def drawCurrentCell(self):
        x,y = self.x*TILE, self.y*TILE    
        drawRect(x,y,TILE,TILE, fill = 'red')
    def draw(self):
        x,y = self.x*TILE, self.y*TILE
        if self.visited:
            drawRect(x,y,TILE,TILE,fill = 'black')
        if self.walls['top']:
            drawLine(x,y,x+TILE,y,fill = 'orange', lineWidth = 2)
        if self.walls['right']:
            drawLine(x+TILE,y,x+TILE,y+TILE,fill = 'orange',lineWidth = 2)
        if self.walls['bottom']:
            drawLine(x+TILE,y+TILE,x,y+TILE,fill = 'orange', lineWidth = 2)
        if self.walls['left']:
            drawLine(x,y+TILE,x,y, fill = 'orange', lineWidth = 2)
    def checkCell(self,x,y):
        #to find index of cell in 1D array knowing its location in 2D array, index = i+j*col
        
        find_index = lambda x,y: x+y*cols
        #check if cell goes off board
        if x<0 or x>cols-1 or y < 0 or y > rows -1:
            return False
        return grid_cells[find_index(x,y)]
    
    def checkNeighbors(self):
        neighbors = []
        top = self.checkCell(self.x,self.y-1)
        right = self.checkCell(self.x+1,self.y)
        bottom = self.checkCell(self.x,self.y+1)
        left = self.checkCell(self.x-1,self.y)
        if top and not top.visited:
            neighbors.append(top)
        if right and not right.visited:
            neighbors.append(right)
        if left and not left.visited:
            neighbors.append(left)
        if bottom and not bottom.visited:
            neighbors.append(bottom)
        #randomly check the neighboring cell:
        return choice(neighbors) if neighbors else False
def removeWalls(current,next):
    dx = current.x - next.x
    if dx == 1:
        current.walls['left'] = False
        next.walls['right'] = False
    elif dx == -1:
        current.walls['right'] = False
        next.walls['left'] = False
    dy = current.y - next.y
    if dy == 1:
        current.walls['top'] = False
        next.walls['bottom'] = False
    elif dy == -1:
        current.walls['bottom'] = False
        next.walls['top'] = False
        
grid_cells = [Cell(col,row) for row in range(rows) for col in range(cols)]




def onAppStart(app):
    app.default_color = 'skyBlue'
    app.width = 600
    app.height = 600 
    app.currentCell = grid_cells[0]
    app.stack = []
#check neighboring cells
    app.keepSearching = True
def redrawAll(app):
    drawRect(0,0,600,600,fill = app.default_color)    
    [cell.draw() for cell in grid_cells]
    app.currentCell.visited = True
    app.currentCell.drawCurrentCell()
    
def onKeyPress(app,key):
    if key == 'p':
        app.keepSearching = not app.keepSearching
def onStep(app): 

    app.nextCell = app.currentCell.checkNeighbors()
    if app.nextCell:
        app.nextCell.visited = True
        app.stack.append(app.currentCell)
        removeWalls(app.currentCell,app.nextCell)
        app.currentCell = app.nextCell
    elif app.stack:
        app.currentCell = app.stack.pop()
def main():
    runApp()
main()