import math
def calc_wins(time, distance):
    wins = 0
    for i in range(time + 1):
        d = (time - i)*(i)
        if d > distance:
            wins += 1
    return wins

def quad_form(a, b, c):
    return (-b + math.sqrt(b**2 - 4*a*c)) // (2*a),  (-b - math.sqrt(b**2 - 4*a*c)) // (2*a)

def parse_as_multiple_races(line):
    return [int(val) for val in line.split() if val.isdigit()]

def parse_as_one_race(line):
    return int("".join([val for val in line.split() if val.isdigit()]))

def boat_races(input):
    num_wins = 1
    with open(input, "r") as input:
        race_data = parse_as_multiple_races(input.read())
        for i in range(len(race_data) // 2):
            num_wins *= calc_wins(race_data[i], race_data[i + (len(race_data) // 2)])
    return num_wins

def boat_race(input):
    lines = open(input, "r")
    data = [parse_as_one_race(line) for line in lines.readlines()]
    roots = quad_form(-1, data[0], -data[1])
    return roots[1] - roots[0]    

print("part1 :", boat_races("d6input.txt"))
print("part2 :", boat_race("d6input.txt"))