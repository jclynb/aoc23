class Pipe:
    def __init__(self, tile, left, right, up, down):
        self.tile = tile
        self.left = left
        self.right = right
        self.up = up
        self.down = down

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
    
    def place_pipe(self, row, col, pipe):
        self.grid[row][col] = pipe
    
    def get_adjacent(self, row, col):
        left =  self.val(row, col - 1)
        right = self.val(row, col + 1)
        up = self.val(row - 1, col)
        down = self.val(row + 1, col)
        tile = self.val(row, col)
        if tile == ".":
            return  None, None, None, None
        elif tile == "|":
            return None, None, up, down
        elif tile == "-":
            return left, right, None, None
        elif tile == "L":
            return None, right, up, None
        elif tile == "J":
            return left, None, up, None
        elif tile == "7":
            return left, None, None, down
        elif tile == "F":
            return None, right, None, down
        elif tile == "S":
            return left, None, up, None
    
    def go_left(self, row, col):
        if self.val(row, col).left and self.is_within_bounds(row, col - 1):
            return (row, col - 1)
        else:
            return None

    def go_right(self, row, col):
        if self.val(row, col).right and self.is_within_bounds(row, col + 1):
            return (row, col + 1)
        else:
            return None
    
    def go_up(self, row, col):
        if self.val(row, col).up and self.is_within_bounds(row - 1, col):
            return (row - 1, col)
        else:
            return None
        
    def go_down(self, row, col):
        if self.val(row, col).down and self.is_within_bounds(row + 1, col):
            return (row + 1, col)
        else:
            return None

    def enclosed_right(self, row, col, path):
        crosses = 0
        while self.is_within_bounds(row, col):
            col += 1
            if (row, col) in path and self.val(row, col).tile not in ["-", "F", "7"]:
                crosses += 1
        if crosses % 2 == 0:
            return False
        else:
            return True

def create_grid(input):    
    grid = Grid(input)
    row_start, col_start = None, None
    for i in range(grid.num_rows):
        for j in range(grid.num_cols):
            if grid.val(i, j) == "S":
                row_start, col_start = i, j
            left, right, up, down = grid.get_adjacent(i, j)
            pipe = Pipe(grid.val(i, j), left, right, up, down)
            grid.place_pipe(i, j, pipe)
    return grid, row_start, col_start

def search_grid(grid, row, col):
    max_distance = 0
    stack = [(row, col, max_distance)]
    visited = set()
    while stack:
        row, col, distance = stack.pop()
        visited.add((row, col))
        left = grid.go_left(row, col)
        right = grid.go_right(row, col)
        up = grid.go_up(row, col)
        down = grid.go_down(row, col)
        if left != None and grid.val(*left).tile != "." and left not in visited:
            stack.append((*left, distance + 1))
            max_distance = max(max_distance, distance + 1)
        if right != None and grid.val(*right).tile != "." and right not in visited:
            stack.append((*right, distance + 1))
            max_distance = max(max_distance, distance + 1)
        if up != None and grid.val(*up).tile != "." and up not in visited:
            stack.append((*up, distance + 1))
            max_distance = max(max_distance, distance + 1)
        if down != None and grid.val(*down).tile != "." and down not in visited:
            stack.append((*down, distance + 1))
            max_distance = max(max_distance, distance + 1)

    print((max_distance + 1) / 2)
    return visited

def scan_grid(grid, path):
    enclosed = 0
    for i in range(grid.num_rows):
        for j in range(grid.num_cols):
            if (i, j) not in path and grid.enclosed_right(i, j, path):
                enclosed += 1
    print(enclosed)

grid, row, col = create_grid("d10input.txt")
path = search_grid(grid, row, col) # part1
scan_grid(grid, path) # part2