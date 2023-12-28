class Path:
    def __init__(self, file_path):
        self.path = self.build_path(file_path)

    def build_path(self, file_path):
        input = open(file_path, "r")
        path = []
        for line in input.readlines():
            _, _, color = line.split()
            direction = color[-2]
            steps = int(color[-7:-2], 16)
            path.append((direction, int(steps)))
        return path

    def count_cubic_meters(self):
        direcmap = {"0":(0, 1), "1":(1, 0), "2":(0, -1), "3":(-1, 0)}
        x = 0
        y = 0
        border = 0
        area = 0
        for direction, steps in self.path:
            dx, dy = direcmap[direction]
            dx *= steps
            dy *= steps
            x += dx
            y += dy
            border += steps
            area += x*dy # Green's Theorem 

            
        return abs(area) + border // 2 + 1

path = Path("d18input.txt")
print(path.count_cubic_meters())
