class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __eq__(self, x, y):
        return self.x == x and self.y == y
    def print(self):
        print("(", self.x, ",", self.y, ")")
    def left(self):
        return Point(self.x, self.y - 1)
    def right(self):
        return Point(self.x, self.y + 1)
    def up(self):
        return Point(self.x - 1, self.y)
    def down(self):
        return Point(self.x + 1, self.y)
    def top_left_adjacent(self):
        return Point(self.x - 1, self.y - 1)
    def top_right_adjacent(self):
        return Point(self.x + 1, self.y - 1)
    def bottom_left_adjacent(self):
        return Point(self.x - 1, self.y + 1)
    def bottom_right_adjacent(self):
        return Point(self.x + 1, self.y + 1)
 
class Grid:
    def __init__(self, file_path):
        self.grid = self.file_to_grid(file_path)
        if not self.grid:
            print("Error. Unable to initalize grid from file.")
        self.num_rows = len(self.grid)
        self.num_cols = len(self.grid[0])
    
    def file_to_grid(self, file_path):
        try:
            with open(file_path, "r") as input:
                lines = input.readlines()
                grid = [list(line.strip()) for line in lines]
                return grid
        except FileNotFoundError:
            print(f"Error: File not found.")
            return None

    def is_within_bounds(self, row, col):
        return 0 <= row < self.num_rows and 0 <= col < self.num_cols

    def val(self, row, col):
        if self.is_within_bounds(row, col):
            return self.grid[row][col]
        else:
            print("Not within bounds")
    
    def scan_adjacent_numbers(self, row, col):
        # returns a number if a symbol is found, else returns 0
        # also returns the length of the number found to reset counter in find_part_numbers
        point = Point(row, col)
        num_list = []
        stack = [point]
        found_symbol = False

        while stack:
            pt = stack.pop()

            if self.is_within_bounds(pt.x, pt.y) and self.val(pt.x, pt.y).isdigit():
                num_list.append(self.val(pt.x, pt.y))
                nxt_pt = pt.right()
                stack.append(nxt_pt)
                if found_symbol == False:
                    found_symbol = self.scan_for_symbol(pt)
        if found_symbol:
            return int("".join(num_list)), len(num_list) - 1
        else:
            return 0, len(num_list) - 1
        
    def scan_star_adjacent_numbers(self, row, col):
        # returns 3 calues: a number if a star symbol is found, the length of num_list to update counter, and a tuple with the star point's x and y coordinates
        # otherwise returns 0, length of num list, and None
        point = Point(row, col)
        num_list = []
        stack = [point]
        found_symbol = False
        star_pt = None

        while stack:
            pt = stack.pop()
            if self.is_within_bounds(pt.x, pt.y) and self.val(pt.x, pt.y).isdigit():
                num_list.append(self.val(pt.x, pt.y))
                nxt_pt = pt.right()
                stack.append(nxt_pt)
                if found_symbol == False:
                    found_symbol, star_pt = self.scan_for_star(pt)

        if found_symbol:
            return int("".join(num_list)), len(num_list) - 1, (star_pt.x, star_pt.y)
        else:
            return 0, len(num_list) - 1, None
    
    def scan_for_symbol(self, point):
        # given a point, returns True if an adjacent symbol is found, otherwise returns False
        stack = [point.up(), point.left(), point.right(), point.down(), point.top_left_adjacent(), point.top_right_adjacent(), point.bottom_left_adjacent(), point.bottom_right_adjacent()]
        while stack:
            pt = stack.pop()
            if self.is_within_bounds(pt.x, pt.y) and self.val(pt.x, pt.y) != "." and not self.val(pt.x, pt.y).isdigit():
                return True
        return False
    
    def scan_for_star(self, point):
        # given a point, returns True and point if an adjacent star symbol is found, otherwise returns False and none
        stack = [point.up(), point.left(), point.right(), point.down(), point.top_left_adjacent(), point.top_right_adjacent(), point.bottom_left_adjacent(), point.bottom_right_adjacent()]
        while stack:
            pt = stack.pop()
            if self.is_within_bounds(pt.x, pt.y) and self.val(pt.x, pt.y) == "*":
                return True, pt
        return False, None
    
# PART 1    
def find_part_numbers(file_path):
    grid = Grid(file_path)
    total_sum = 0
    counter = 0

    for i in range(grid.num_rows):
        for j in range(grid.num_cols):
            if counter != 0:
                counter -= 1
            elif grid.val(i, j).isdigit(): # hit a number
                num, num_len, = grid.scan_adjacent_numbers(i, j) # returns 0 if the number is not adjacent to a symbol
                total_sum += num
                counter = num_len
    return total_sum

# PART 2
def find_gear_numbers(file_path):
    grid = Grid(file_path)
    gears = {}
    total_sum = 0
    counter = 0

    for i in range(grid.num_rows):
        for j in range(grid.num_cols):
            if counter != 0:
                counter -= 1
            elif grid.val(i, j).isdigit(): # hit a number
                num, num_len, star_pt = grid.scan_star_adjacent_numbers(i, j) # returns the number, the length of the number - 1 (i.e. 50 is length 2), and the coords of the star symbol
                if star_pt and star_pt in gears:
                    gears[star_pt].append(num)
                elif star_pt:
                    gears[star_pt] = [num]
                counter = num_len
            
    for vals in gears.values():
        if len(vals) == 2:
            total_sum += (vals[0] * vals[1])
    return total_sum

part1_sum = find_part_numbers("d3input.txt")
part2_sum = find_gear_numbers("d3input.txt")
print("Part 1: ", part1_sum)
print("Part 2: ", part2_sum)
