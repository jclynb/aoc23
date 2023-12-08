def parse_line(line):
    num_list = [int(x) for x in line.split()]
    return num_list

def sum_projected(list, last_val):
    l = 0
    r = 1
    sum_list = []
    while r <= len(list) - 1:
        sum_list.append(list[r] - list[l])
        r += 1
        l += 1
    if not all([x == 0 for x in sum_list]):
        last_val += sum_list[-1]
        return sum_projected(sum_list, last_val)
    else:
        return last_val
    
def extrapolate_backwards(list, last_vals):
    l = 0
    r = 1
    blist = []
    while r <= len(list) - 1:
        blist.append(list[r] - list[l])
        r += 1
        l += 1
    if not all([x == 0 for x in blist]):
        last_vals.append(blist[0])
        return extrapolate_backwards(blist, last_vals)
    else:
        val = 0
        last_vals.reverse()
        for num in last_vals:
            val = (num - val)
        return val
    
def solve(input):
    input = open(input, "r")
    projected = 0
    extrapolated = 0
    for line in input:
        num_list = parse_line(line)
        projected += sum_projected(num_list, num_list[-1]) # part 1 : project forward
        extrapolated += extrapolate_backwards(num_list, [num_list[0]]) # part 2 : extrapolate backward
    return projected, extrapolated

print(solve("d9input.txt"))
