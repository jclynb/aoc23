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
        
    def move_north(self, row, col):
        while row > 0 and self.grid[row - 1][col] == ".":
            self.grid[row - 1][col] = "O"
            self.grid[row][col] = "."
            row -= 1

    def move_west(self, row, col):
        while col > 0 and self.grid[row][col - 1] == ".":
            self.grid[row][col - 1] = "O"
            self.grid[row][col] = "."
            col -= 1

    def move_south(self, row, col):
        while row < self.num_rows - 1 and self.grid[row + 1][col] == ".":
            self.grid[row + 1][col] = "O"
            self.grid[row][col] = "."
            row += 1

    def move_east(self, row, col):
        while col < self.num_cols - 1 and self.grid[row][col + 1] == ".":
            self.grid[row][col + 1] = "O"
            self.grid[row][col] = "."
            col += 1

    def tilt(self):
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                if grid.val(i, j) == "O":
                    self.move_north(i, j)

    def spin(self):
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                if grid.val(i, j) == "O":
                    self.move_north(i, j)

        for i in range(self.num_rows):
            for j in range(self.num_cols):
                if grid.val(i, j) == "O":
                    self.move_west(i, j)  

        for i in range(self.num_rows):
            for j in range(self.num_cols):
                row = self.num_rows - i - 1
                if grid.val(row, j) == "O":
                    self.move_south(row, j)  
        
        for i in range(self.num_rows):
            for j in range(self.num_cols + 1):
                col = self.num_cols - j - 1
                if grid.val(i, col) == "O":
                    self.move_east(i, col)
                    
    def sum_loads(self):
        sum = 0
        sums = {}
        for i in range(grid.num_rows):
            for j in range(grid.num_cols):
                if grid.val(i,j) == "O":
                    sum += (grid.num_rows - i)
                    if sum not in sums:
                        sums[sum] = x
                    else:
                        print("cycle", x, "load", sum, "prev cycle", sums[sum])
        print(sum)
        
grid = Grid("d14input.txt")
# grid.tilt()

for x in range(10000):
    grid.spin()
    grid.sum_loads()