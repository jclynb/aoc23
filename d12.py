import math
from functools import cache
import itertools

def scan_group(group, counts):
    arrangement = 0
    replacements = [".", "#"]
     # Generate all possible replacements for '?'
    replacement_combinations = itertools.product(replacements, repeat=len(group))
    for comb in list(replacement_combinations):
        comb = "".join(comb)
        comb = comb.split(".")
        comb = [x for x in comb if x != ""]
        if len(comb) != len(counts):
            continue
        else:
            if all([len(group) == count for group, count in zip(comb, counts)]):
                arrangement += 1
    return arrangement

def parse_file(file):
    sum = 0
    input = open(file, "r")
    for line in input.readlines():
        line = line.strip().split()
        springs = line[0]
        springs = springs.split(".")
        springs = [x for x in springs if x != ""]
        counts = [int(x) for x in line[1].split(",")]
        print(springs)
        print(counts)
        print(scan_group(springs, counts))
    

parse_file("d12test.txt")
