import math
class Node:
    def __init__(self, val, left, right):
        self.val = val
        self.left = left
        self.right = right
        self.graph = None
    
    def go_left(self):
        return self.graph.get_node(self.left)

    def go_right(self):
        return self.graph.get_node(self.right)

class Graph:
    def __init__(self, nodes):
        self.nodes = {}
        for node in nodes:
            self.nodes[node.val] = node
            node.graph = self
    
    def get_node(self, node_name):
        return self.nodes[node_name]
    
def parse_data(input):
    node_list = []
    lines = open(input, "r")
    for line in lines.readlines():
        if line == "\n":
            continue
        elif not " = " in line:
            directions = line.strip()
        else:
            node = line.strip(")\n").split(" = ") 
            left, right = node[1].strip("(").split(", ")
            node_list.append(Node(node[0], left, right))
    return directions, node_list

def search_graph(node, directions):
    steps = 0
    while not node.val.endswith("Z"):
        for direction in directions:
            if direction == "L":
                node = node.go_left()
                steps += 1
            elif direction == "R":
                node = node.go_right()
                steps += 1
    return steps

def calc_steps(input):
    directions, nodes = parse_data(input)
    graph = Graph(nodes)
    # part1: curr_node = graph.get_node("AAA")
    
    start_nodes = []
    end_nodes = []
    for node in graph.nodes:
        if node.endswith("A"): 
            start_nodes.append(graph.get_node(node))
        elif node.endswith("Z"):
            end_nodes.append(graph.get_node(node))

    step_list = [search_graph(node, directions) for node in start_nodes]
    return math.lcm(*[node for node in step_list])

print("part2: ", calc_steps("d8inpuut.txt"))