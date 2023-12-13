class Grid:
    def __init__(self, grid):
        self.grid = grid
        self.num_rows = len(self.grid)
        self.num_cols = len(self.grid[0])
        self.mirror_row = self.scan_rows()
        self.mirror_col = self.scan_cols()
        self.smudge_row = self.scan_smudge_rows()
        self.smudge_col = self.scan_smudge_cols()
    
    def is_within_bounds(self, row, col):
        return 0 <= row < self.num_rows and 0 <= col < self.num_cols
    
    def val(self, row, col):
        if self.is_within_bounds(row, col):
            return self.grid[row][col]
        else:
            return None
        
    def scan_rows(self):
        for r1, r2 in zip(range(self.num_rows), range(1, self.num_rows)):
            symmetric = all(self.val(r1, c) == self.val(r2, c) for c in range(self.num_cols))
            if symmetric:
                if self.check_r_mirror(r1, r2):
                    return r1 + 1
        return 0
    
    def scan_cols(self):
        for c1, c2 in zip(range(self.num_cols), range(1, self.num_cols)):
            symmetric = all(self.val(r, c1) == self.val(r, c2) for r in range(self.num_rows))
            if symmetric:
                if self.check_c_mirror(c1, c2):
                    return c1 + 1
        return 0
    
    def scan_smudge_rows(self):
        for r1, r2 in zip(range(self.num_rows), range(1, self.num_rows)):
            smudges = False
            symmetric = True
            for c in range(self.num_cols):
                if self.val(r1, c) != self.val(r2, c) and not smudges:
                    smudges = True
                elif self.val(r1, c) != self.val(r2, c) and smudges:
                    symmetric = False
            if symmetric and ((r1 + 1) != self.mirror_row):
                if self.check_r_smudge(r1, r2):
                    return r1 + 1
        return 0
    
    def scan_smudge_cols(self):
        for c1, c2 in zip(range(self.num_cols), range(1, self.num_cols)):
            smudges = False
            symmetric = True
            for r in range(self.num_rows):
                if self.val(r, c1) != self.val(r, c2) and not smudges:
                    smudges = True
                elif self.val(r, c1) != self.val(r, c2) and smudges:
                    symmetric = False
            if symmetric and (c1 + 1) != self.mirror_col:
                if self.check_c_smudge(c1, c2):
                    return c1 + 1
        return 0

    def check_r_mirror(self, row1, row2):
        symmetric = True
        while symmetric and row1 > 0 and row2 < self.num_rows - 1:
            row1 -= 1
            row2 += 1
            symmetric = all(self.val(row1, c) == self.val(row2, c) for c in range(self.num_cols))
            if symmetric == False:
                return False
        return True
    
    def check_r_smudge(self, row1, row2):
        smudges = False
        while row1 > 0 and row2 < self.num_rows - 1:
            row1 -= 1
            row2 += 1
            for c in range(self.num_cols):
                if self.val(row1, c) != self.val(row2, c) and not smudges:
                    smudges = True
                elif self.val(row1, c) != self.val(row2, c) and smudges:
                    return False
        return True
    
    def check_c_mirror(self, col1, col2):
        symmetric = True
        while symmetric and col1 > 0 and col2 < self.num_cols - 1:
            col1 -= 1
            col2 += 1
            symmetric = all(self.val(r, col1) == self.val(r, col2) for r in range(self.num_rows))
            if symmetric == False:
                return False
        return True
    
    def check_c_smudge(self, col1, col2):
        smudges = False
        while col1 > 0 and col2 < self.num_cols - 1:
            col1 -= 1
            col2 += 1
    
            for r in range(self.num_rows):
                if self.val(r, col1) != self.val(r, col2) and not smudges:
                    smudges = True
                elif self.val(r, col1) != self.val(r, col2) and smudges:
                    return False
        return True

def parse_input(input):
    input = open(input, "r")
    grids = []
    grid = []
    for line in input.readlines():
        if line != "\n":
            grid.append(list(line.strip()))
        else:
            g = Grid(grid)
            grids.append(g)
            grid = []
    return grids

grids = parse_input("d13input.txt")
sum1 = 0
sum2 = 0
for grid in grids:
    sum1 += (grid.mirror_col + 100*grid.mirror_row)
    sum2 += (grid.smudge_col + 100*grid.smudge_row)
print(sum1)
print(sum2)
