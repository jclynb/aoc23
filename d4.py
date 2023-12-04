def parse_line(line):
    parts = line.split(":")
    card_num = int(parts[0].strip("Card "))
    groups = parts[1].strip().split(" | ")
    winning_nums = set()
    my_nums = set()

    for group in groups:
        numbers = [int(num) for num in group.split() if num.isdigit()]
        if numbers:
            if winning_nums:
                my_nums.update(numbers)
            else:
                winning_nums.update(numbers)
    return card_num, winning_nums, my_nums

def get_score(file_path):
    data = open(file_path, "r")
    card_copies = {}
    total_score = 0
    total_copies = 0
    for line in data.readlines():
        card_num, winning_nums, my_nums = parse_line(line)
        matches = winning_nums.intersection(my_nums)
        if card_num in card_copies:
            new_copies = (card_copies[card_num] + 1)
        else:
            new_copies = 1
            card_copies[card_num] = 0
        if matches:
            score = 2**(len(matches) - 1)
            for i in range(1, len(matches) + 1):
                if (card_num + i) in card_copies:
                    card_copies[card_num + i] += new_copies
                else:
                    card_copies[card_num + i] = new_copies
        else:
            score = 0
        total_score += score
        
    for val in card_copies.values():
        total_copies += (val + 1)

    data.close()
    return total_score, total_copies

part1, part2 = get_score("d4input.txt")
print("part1: ", part1)
print("part2: ", part2)
