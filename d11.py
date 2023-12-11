import itertools
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __eq__(self, x, y):
        return self.x == x and self.y == y
    def manhattan_distance(self, point):
        return abs(self.x - point.x) + abs(self.y - point.y)
    
class Grid:
    def __init__(self, file_path):
        self.grid = self.file_to_grid(file_path)
        self.num_rows = len(self.grid)
        self.num_cols = len(self.grid[0])
        self.empty_rows = []
        self.empty_cols = []
        self.galaxy_combinations = []
    
    def file_to_grid(self, file_path):
        with open(file_path, "r") as input:
            grid = []
            lines = input.readlines()
            grid = [list(line.strip()) for line in lines]
            return grid
    
    def get_empty_rows(self):
        for i, row in enumerate(self.grid):
            # Check empty space in rows
            if all([x == "." for x in row]):
                self.empty_rows.append(i)
        
    def get_empty_cols(self):
        for col in range(self.num_cols):
            found_galaxies = False
            for row in range(self.num_rows):
                if self.grid[row][col] == "#":
                    found_galaxies = True
            if not found_galaxies:
                self.empty_cols.append(col)

    def translate_point(self, point, shift):
        shift_x = 0
        shift_y = 0
        sorted(self.empty_rows)
        sorted(self.empty_cols)
        for row in self.empty_rows:
            if point.x > row:
                shift_x += shift
            else:
                break
        for col in self.empty_cols:
            if point.y > col:
                shift_y += shift
            else:
                break
        return Point(point.x + shift_x, point.y + shift_y)

    def get_galaxy_combinations(self, shift):
        galaxy_list = []
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                if self.grid[row][col] == "#":
                    galaxy_list.append(self.translate_point(Point(row, col), shift))
        self.galaxy_combinations = list(itertools.combinations(galaxy_list, 2))

    def is_within_bounds(self, point):
        return 0 <= point.x < self.num_rows and 0 <= point.y < self.num_cols
    
    def val(self, point):
        if self.is_within_bounds(point.x, point.y):
            return self.grid[point.x][point.y]
        else:
            return None
        
def shortest_path(input, shift):    
    grid = Grid(input)    
    grid.get_empty_rows()
    grid.get_empty_cols()
    grid.get_galaxy_combinations(shift)

    sum_distance = 0
    for gal1, gal2 in grid.galaxy_combinations:
        sum_distance += gal1.manhattan_distance(gal2)
    
    return sum_distance

print(shortest_path("d11input.txt", 999999))