from cmu_graphics import*
from random import choice

TILE = 90
cols, rows = 900 // TILE, 900 // TILE

class Cell:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        self.visited = False
        self.thickness = 4
        self.cols = 900//TILE
    def draw(self):
        x,y = self.x*TILE, self.y*TILE
        
        if self.walls['top']:
            drawLine(x,y,x+TILE,y,fill = 'orange', lineWidth = 2)
        if self.walls['right']:
            drawLine(x+TILE,y,x+TILE,y+TILE,fill = 'orange',lineWidth = 2)
        if self.walls['bottom']:
            drawLine(x+TILE,y+TILE,x,y+TILE,fill = 'orange', lineWidth = 2)
        if self.walls['left']:
            drawLine(x,y+TILE,x,y, fill = 'orange', lineWidth = 2)

    # def get_rects(self):
    #     rects = []
    #     x, y = self.x * TILE, self.y * TILE
    #     if self.walls['top']:
    #         rects.append(pygame.Rect( (x, y), (TILE, self.thickness) ))
    #     if self.walls['right']:
    #         rects.append(pygame.Rect( (x + TILE, y), (self.thickness, TILE) ))
    #     if self.walls['bottom']:
    #         rects.append(pygame.Rect( (x, y + TILE), (TILE , self.thickness) ))
    #     if self.walls['left']:
    #         rects.append(pygame.Rect( (x, y), (self.thickness, TILE) ))
    #     return rects

    def check_cell(self, x, y):
        find_index = lambda x, y: x + y * cols
        if x < 0 or x > cols - 1 or y < 0 or y > rows - 1:
            return False
        return self.grid_cells[find_index(x, y)]

    def check_neighbors(self, grid_cells):
        self.grid_cells = grid_cells
        neighbors = []
        top = self.check_cell(self.x, self.y - 1)
        right = self.check_cell(self.x + 1, self.y)
        bottom = self.check_cell(self.x, self.y + 1)
        left = self.check_cell(self.x - 1, self.y)
        if top and not top.visited:
            neighbors.append(top)
        if right and not right.visited:
            neighbors.append(right)
        if bottom and not bottom.visited:
            neighbors.append(bottom)
        if left and not left.visited:
            neighbors.append(left)
        return choice(neighbors) if neighbors else False


def remove_walls(current, next):
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

def generate_maze():
    grid_cells = [Cell(col, row) for row in range(rows) for col in range(cols)]
    current_cell = grid_cells[0]
    array = []
    break_count = 1

    while break_count != len(grid_cells):
        current_cell.visited = True
        next_cell = current_cell.check_neighbors(grid_cells)
        if next_cell:
            next_cell.visited = True
            break_count += 1
            array.append(current_cell)
            remove_walls(current_cell, next_cell)
            current_cell = next_cell
        elif array:
            current_cell = array.pop()
    grid_cells[-1].walls['right'] = False
    return grid_cells