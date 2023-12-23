from collections import deque
class Beam:
    def __init__(self, direction, row, col, grid):
        self.direction = direction
        self.row = row
        self.col = col
        self.grid = grid
    
    def __hash__(self):
        return hash((self.direction, self.col, self.row))
    
    def __eq__(self, other):
        if isinstance(other, Beam):
            return (self.direction == other.direction and self.row == other.row and self.col == other.col)
        return False
    
    def move(self):
        if self.direction == "right":
            if self.grid.is_within_bounds(self.row, self.col + 1):
                self.col += 1
                return self
            else:
                return 0
        elif self.direction == "left":
            if self.grid.is_within_bounds(self.row, self.col - 1):
                self.col -= 1
                return self
            else:
                return 0
        elif self.direction == "up":
            if self.grid.is_within_bounds(self.row - 1, self.col):
                self.row -= 1
                return self
            else:
                return 0
        elif self.direction == "down":
            if self.grid.is_within_bounds(self.row + 1, self.col):
                self.row += 1
                return self
            else:
                return 0
        else:
            return 0

    def check_direction(self):
        encounter = self.grid.val(self.row, self.col)
        if encounter == "\\" and self.direction == "right":
            self.direction = "down"
            return self, 0
        elif encounter == "\\" and self.direction == "left":
            self.direction = "up"
            return self, 0
        elif encounter == "\\" and self.direction == "up":
            self.direction = "left"
            return self, 0
        elif encounter == "\\" and self.direction == "down":
            self.direction = "right" 
            return self, 0
        elif encounter == "/" and self.direction == "right":
            self.direction = "up"
            return self, 0 
        elif encounter == "/" and self.direction == "left":
            self.direction = "down"
            return self, 0
        elif encounter == "/" and self.direction == "up":
            self.direction = "right"
            return self, 0
        elif encounter == "/" and self.direction == "down":
            self.direction = "left" 
            return self, 0
        elif encounter == "|" and (self.direction == "left" or self.direction == "right"):
            beam1 = Beam("up", self.row, self.col, self.grid)
            beam2 = Beam("down", self.row, self.col, self.grid)
            return beam1, beam2
        elif encounter == "-" and (self.direction == "up" or self.direction == "down"):
            beam1 = Beam("left", self.row, self.col, self.grid)
            beam2 = Beam("right", self.row, self.col, self.grid)
            return beam1, beam2
        else:
            return self, 0

class Grid:
    def __init__(self, file_path):
        self.grid = self.file_to_grid(file_path)
        self.num_rows = len(self.grid)
        self.num_cols = len(self.grid[0])
    
    def file_to_grid(self, file_path):
        with open(file_path, "r") as input:
            grid = []
            lines = input.readlines()
            grid = [list(line.strip()) for line in lines]
            return grid
        
    def is_within_bounds(self, row, col):
        return 0 <= row < self.num_rows and 0 <= col < self.num_cols
    
    def val(self, row, col):
        if self.is_within_bounds(row, col):
            return self.grid[row][col]
        else:
            return None

def count_energized_tiles(beam):    
    q = deque([beam])
    visited = set()
    energized = set()
    while q:
        beam = q.popleft()
        if beam and beam not in visited:
            visited.add(beam)
            energized.add((beam.row, beam.col))
            beam1, beam2 = beam.check_direction()
            if beam1:
                q.append(beam1.move())
            if beam2:
                q.append(beam2.move())
    return len(energized)

def part2(input):
    grid = Grid(input)
    max_energized = 0
    for i in range(grid.num_rows):
        beam = Beam("left", i, 0, grid)
        max_energized = max(max_energized, count_energized_tiles(beam))
    for i in range(grid.num_rows):
        beam = Beam("right", i, grid.num_cols - 1, grid)
        max_energized = max(max_energized, count_energized_tiles(beam))
    for j in range(grid.num_cols):
        beam = Beam("down", 0, j, grid)
        max_energized = max(max_energized, count_energized_tiles(beam))
    for j in range(grid.num_rows):
        beam = Beam("up", grid.num_rows - 1, j, grid)
        max_energized = max(max_energized, count_energized_tiles(beam))
    print(max_energized)

part2("d16input.txt")