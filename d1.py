class getCalibration:
    def __init__(self, input):
        self.input = open("input.txt", "r")
        self.word_map = {"one" : 1,
                        "two": 2,
                        "three": 3,
                        "four": 4,
                        "five": 5,
                        "six": 6,
                        "seven": 7,
                        "eight": 8,
                        "nine": 9
                        }
        self.valid_chars = {"e": 5, "f": 4, "n": 4, "o": 3, "s": 5, "t": 5} # spelled out words 1-9 start with these 6 letters, 
                                                                            # maps to max word length (i.e."s" could be six or seven, max len 5)

    def find_num_vals(self):
        # Uses two pointers to find the first numeric char and then the second
        # returns int total_sum
        total_sum = 0
        for line in self.input.readlines():
            l = 0
            r = len(line) - 1
            digit_1 = 10
            digit_2 = 0
            left_found = False
            right_found = False

            while l <= r:
                if not left_found and line[l].isnumeric():
                    digit_1 *= int(line[l])
                    left_found = True
                elif not left_found:
                    l += 1

                if not right_found and line[r].isnumeric():
                    digit_2 += int(line[r])
                    right_found = True
                elif not right_found:
                    r -= 1

                if left_found and right_found:
                    break
            
            total_sum += (digit_1 + digit_2)
            self.input.close()

        return total_sum
    
    def check_spelled_word(self, line, idx):
        # returns int 1-9 if the word is a valid spelled-out digit
        # else returns int 0
        curr_word = line[idx]
        r = idx + 1
        while r < len(line) - 1 and len(curr_word) < self.valid_chars[line[idx]]:
            curr_word += line[r]
            if curr_word in self.word_map:
                return self.word_map[curr_word]
            else:
                r += 1
        return 0


    def get_first_digit(self, line):
        # reads line left to right to find first digit
        # returns an int
        # returns 0 if error
        for idx, char in enumerate(line):
            if char.isnumeric():
                return 10 * int(char) 
            elif char in self.valid_chars:
                curr_word = self.check_spelled_word(line, idx)
                if curr_word != 0:
                    return 10 * curr_word

        return 0

    def get_second_digit(self, line):
        # reads line right to left to find the second digit
        # returns an int
        # returns 0 if error
        idx = len(line) - 1

        while idx >= 0:
            if line[idx].isnumeric():
                return int(line[idx])
            elif line[idx] in self.valid_chars:
                curr_word = self.check_spelled_word(line, idx)
                if curr_word != 0:
                    return curr_word
                else:
                    idx -= 1
            else:
                idx -= 1
        return 0

    
    def find_spelled_vals(self):
        self.input = open("input.txt")
        total_sum = 0
        
        for line in self.input.readlines():
            digit_1 = self.get_first_digit(line)
            digit_2 = self.get_second_digit(line)
            total_sum += (digit_1 + digit_2)

        self.input.close()
        return total_sum
          
if __name__ == "__main__":
    solver = getCalibration("input.txt")
    part1 = solver.find_num_vals()
    part2 = solver.find_spelled_vals()

    print("part1: ", part1)
    print("part2: ", part2)