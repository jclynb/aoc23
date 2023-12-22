def hash(string):
    curr = 0
    for char in string:
        if char == "=":
            return curr, int(string[-1])
        elif char == "-":
            return curr, 10
        else:
            curr += ord(char)
            curr *= 17
            curr = curr % 256

def parse_input(input):
    boxes = {}
    lines = open(input, "r")
    for line in lines.readlines():
        strings = line.strip().split(",")
        for string in strings:
            label, val = hash(string)
            if val < 10 and label not in boxes:
                boxes[label] = {string[:-2]: val}
            elif val < 10:
                boxes[label][string[:-2]] = val
            else:
                if label in boxes and string[:-1] in boxes[label]:
                    del boxes[label][string[:-1]]
    return boxes

def sum_focus_power(boxes):            
    power = 0
    for key in boxes:
        inner_dict = boxes[key]
        for i, inner_val in enumerate(inner_dict.values()):
            power += (key + 1) * inner_val * (i + 1)
    return power

print(sum_focus_power(parse_input("d15input.txt")))