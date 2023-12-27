import heapq

class State:
    def __init__(self, row, col, dx, dy, distance):
        self.x = row
        self.y = col
        self.dx = dx
        self.dy = dy
        self.distance = distance

    def __lt__(self, other):
        return self.x < other.x
    
    def __eq__(self, other):
        return (self.x == other.x and self.y == other.y and self.dx == other.dx and self.dy == other.dy and self.distance == other.distance)
    
    def __hash__(self):
        return hash((self.x, self.y, self.dx, self.dy, self.distance))

class Grid:
    def __init__(self, file_path):
        self.grid = self.file_to_grid(file_path)
        self.num_rows = len(self.grid)
        self.num_cols = len(self.grid[0])
        self.end_row = self.num_rows - 1
        self.end_col = self.num_cols - 1
    
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

def dijkstra(grid):
    visited = set()
    heap = []

    def add_state(visited, heap, weight, x, y, dx, dy, distance): 
        # Move to next position
        x += dx
        y += dy
        if grid.is_within_bounds(x, y):
            new_weight = weight + int(grid.val(x, y))
            # If we reached the bottom right corner of the grid, print shortest path
            if x == grid.end_row and y == grid.end_col: 
                print("shortest path: ", new_weight)
                return new_weight
            state = State(x, y, dx, dy, distance)
            if state not in visited and new_weight:
                heapq.heappush(heap, (new_weight, state)) 
                visited.add(state)
        return 0

    # Start at (0, 0) and add Right and Down states to priority queue
    add_state(visited, heap, weight=0, x=0, y=0, dx=0, dy=1, distance=1) # (0, 0) -> (0, 1)
    add_state(visited, heap, weight=0, x=0, y=0, dx=1, dy=0, distance=1) # (0, 0) -> (1, 0)
        
    while heap:
        weight, state = heapq.heappop(heap)

        # If less than 4, go straight
        if state.distance < 4:
            straight = add_state(visited, heap, weight, state.x, state.y, state.dx, state.dy, state.distance + 1) 
            if straight:
                return straight
        else:
            # Go left and right
            left = add_state(visited, heap, weight, state.x, state.y, -state.dy, state.dx, 1) 
            right = add_state(visited, heap, weight, state.x, state.y, state.dy, -state.dx, 1) 
            if left:
                return left
            elif right:
                return right
            # If less than 10, also go straight
            if state.distance < 10:
                straight = add_state(visited, heap, weight, state.x, state.y, state.dx, state.dy, state.distance + 1) 
                if straight:
                    return straight

    
grid = Grid("d17input.txt")
distance = dijkstra(grid)