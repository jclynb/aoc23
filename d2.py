import re

def sum_game_ids(red_num, green_num, blue_num, input_file):
    input = open(input_file, "r")
    game_pattern = r'(Game )(\d+):' 
    color_pattern = r'(\d+) (green|red|blue)(;|,|)'
    total_sum = 0

    for line in input.readlines():
        game_match = re.findall(game_pattern, line)
        game_id = [int(match[1]) for match in game_match]

        color_match = re.findall(color_pattern, line)
        valid_game = True

        for match in color_match:
            num = int(match[0])
            color = match[1]
            if color == "red":
                if num > red_num:
                    valid_game = False
                    break
            elif color == "green":
                if num > green_num:
                    valid_game = False
                    break
            else:
                if num > blue_num:
                    valid_game = False
                    break
        if valid_game:
            total_sum += game_id[0] 
    input.close()
    return total_sum

def power_sum(input_file):
    input = open(input_file, "r")
    game_pattern = r'(Game )(\d+):' 
    color_pattern = r'(\d+) (green|red|blue)(;|,|)'
    total_sum = 0

    for line in input.readlines():
        game_match = re.findall(game_pattern, line)
        game_id = [int(match[1]) for match in game_match]

        color_match = re.findall(color_pattern, line)
        red_max = 0
        green_max = 0
        blue_max = 0

        for match in color_match:
            num = int(match[0])
            color = match[1]
            if color == "red":
                red_max = max(num, red_max)
            elif color == "green":
                green_max = max(num, green_max)
            else:
                blue_max = max(num, blue_max)

        total_sum += (red_max * blue_max * green_max)
    input.close()    
    return total_sum              


part1_sum = sum_game_ids(12, 13, 14, "d2input.txt")
part2_sum = power_sum("d2input.txt")
print("part1: ", part1_sum)    
print("part2: ", part2_sum)


