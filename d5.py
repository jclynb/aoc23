class Seed:
    def __init__(self, seed, map):
        self.seed = seed
        self.soil = self.transform(map.soil, self.seed)
        self.fertilizer = self.transform(map.fert, self.soil)
        self.water = self.transform(map.water, self.fertilizer)
        self.light = self.transform(map.light, self.water)
        self.temp = self.transform(map.temp, self.light)
        self.humidity = self.transform(map.hum, self.temp)
        self.location = self.transform(map.loc, self.humidity)

    def transform(self, map, source):
        result = source
        for image in map:
            if image.source.start <= result <= image.source.end:
                result = image.dest.start + (result - image.source.start)
                break
        return result
    
class Maps:
    def __init__(self, soil, fert, water, light, temp, hum, loc):
        self.soil = sorted(soil, key=sort_by_source)
        self.fert = sorted(fert, key=sort_by_source)
        self.water = sorted(water, key=sort_by_source)
        self.light = sorted(light, key=sort_by_source)
        self.temp = sorted(temp, key=sort_by_source)
        self.hum = sorted(hum, key=sort_by_source)
        self.loc = sorted(loc, key=sort_by_source)

class imageRanges: 
    def __init__(self, input):
        self.dest = Range(int(input[0]), int(input[0] + int(input[2]) - 1))
        self.source = Range(int(input[1]), int(input[1]) + int(input[2]) - 1)

def sort_by_source(obj):
    return obj.source.start

class Range:
    def __init__(self, start, end):
        self.start = start
        self.end = end
    def __hash__(self):
        return hash((self.start, self.end))
    def __eq__(self, other):
        if isinstance(other, Range):
            return (self.start == other.start and self.end == self.end)
    def overlap(self, other):
        return self.start < other.end and self.start < other.end
    
def parse_seeds(input):
    seeds = []
    soil_map = []
    fert_map = []
    water_map = []
    light_map = []
    temp_map = []
    hum_map = []
    loc_map = []

    lines = input.split("\n")

    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith("seeds"):
            seeds = [int(num) for num in line.split(": ")[1].split()]
        elif line.startswith("seed-to-soil map:"):
            name = "seed-to-soil-map"
            current_list = soil_map
        elif line.startswith("soil-to-fertilizer map:"):
            name = "soil-to-fertilizer map"
            current_list = fert_map
        elif line.startswith("fertilizer-to-water map:"):
            name = "fertilizer-to-water map"
            current_list = water_map
        elif line.startswith("water-to-light map:"):
            name = "water-to-light map"
            current_list = light_map
        elif line.startswith("light-to-temperature map:"):
            name = "light-to-temperature map"
            current_list = temp_map
        elif line.startswith("temperature-to-humidity map:"):
            name = "temperature-to-humidity map"
            current_list = hum_map
        elif line.startswith("humidity-to-location map:"):
            name = "humidity-to-location map"
            current_list = loc_map
        elif name:
            data = [int(num) for num in line.split()]
            current_list.append(imageRanges(data))
    map = Maps(soil_map, fert_map, water_map, light_map, temp_map, hum_map, loc_map)

    return [Seed(seed, map) for seed in seeds]

def parse_seed_ranges(input):
    list_seeds = []
    soil_map = []
    fert_map = []
    water_map = []
    light_map = []
    temp_map = []
    hum_map = []
    loc_map = []

    lines = input.split("\n")

    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith("seeds"):
            seeds = [int(num) for num in line.split(": ")[1].split()]
            for i in range(0, len(seeds), 2):
                list_seeds.append((seeds[i], seeds[i+1]))
        elif line.startswith("seed-to-soil map:"):
            name = "seed-to-soil-map"
            current_list = soil_map
        elif line.startswith("soil-to-fertilizer map:"):
            name = "soil-to-fertilizer map"
            current_list = fert_map
        elif line.startswith("fertilizer-to-water map:"):
            name = "fertilizer-to-water map"
            current_list = water_map
        elif line.startswith("water-to-light map:"):
            name = "water-to-light map"
            current_list = light_map
        elif line.startswith("light-to-temperature map:"):
            name = "light-to-temperature map"
            current_list = temp_map
        elif line.startswith("temperature-to-humidity map:"):
            name = "temperature-to-humidity map"
            current_list = hum_map
        elif line.startswith("humidity-to-location map:"):
            name = "humidity-to-location map"
            current_list = loc_map
        elif name:
            data = [int(num) for num in line.split()]
            current_list.append(imageRanges(data))
    map = Maps(soil_map, fert_map, water_map, light_map, temp_map, hum_map, loc_map)     
    return [SeedRange(seeds[0], seeds[1], map) for seeds in list_seeds]

class SeedRange:
    def __init__(self, seed, range, map):
        self.seed = {Range(seed, (seed + range - 1))}
        self.soil = self.transform(map.soil, self.seed)
        self.fertilizer = self.transform(map.fert, self.soil)
        self.water = self.transform(map.water, self.fertilizer)
        self.light = self.transform(map.light, self.water)
        self.temp = self.transform(map.temp, self.light)
        self.humidity = self.transform(map.hum, self.temp)
        self.location = self.transform(map.loc, self.humidity)

    def transform(self, map, seed_range_numbers):

        mapped_ranges = set()
        for range in seed_range_numbers: # seed ranges, soil ranges, etc
            for i, image in enumerate(map): # images contain source-to-destination ranges 
                # If the seed range has no overlap with the source_range
                if not range.overlap(image.source): 
                  continue
                # If the seed range is inside source_range
                elif image.source.start <= range.start and range.end <= image.source.end:
                    start = image.dest.start + (range.start - image.source.start)
                    end = image.dest.start + (range.end - image.source.start)
                    mapped_ranges.add(Range(start, end))
                    break
                # source_range is subset of curr_range
                elif image.source.start <= range.start and image.source.end >= range.end:
                    mapped_range = Range(image.dest.start, image.dest.end)
                    sliceleft = Range(range.start, image.source.start - 1)
                    sliceright = Range(image.source.end + 1, range.end)
                    mapped_ranges.add(sliceleft)
                    mapped_ranges.add(mapped_range)
                    mapped_ranges.update(self.transform(map[i+1:], [sliceright])) # see if sliceright range overlaps with larger source ranges
                    break
                # curr_range overlaps only on left side
                elif image.source.start <= range.start and range.end > image.source.end:
                    mapped_range = Range(image.dest.start + (range.start - image.source.start), image.dest.end)
                    mapped_ranges.add(mapped_range)
                    slice = Range(image.source.end + 1, range.end) 
                    mapped_ranges.update(self.transform(map[i+1:], [slice])) # see if slice range overlaps with larger source ranges
                    break
                # curr_range overlaps only on right side
                elif image.source.start > range.start and range.end <= image.source.end:
                    mapped_range = Range(image.dest.start, image.dest.start + (range.end - image.source.start))
                    slice = Range(range.start, image.source.start -  1)
                    mapped_ranges.add(slice)
                    mapped_ranges.add(mapped_range)
                    break
            # curr_range didn't overlap with any source_ranges
            if len(mapped_ranges) == 0:
                mapped_ranges.add(range)
        return mapped_ranges

def part1(input):
    with open(input, "r") as data:
        seed_list = parse_seeds(data.read())
        return min(seed.location for seed in seed_list)
    
def part2(input):
    with open(input, "r") as data:
        seed_list = parse_seed_ranges(data.read())
        min_loc = float("infinity")
        for seed in seed_list:
            for val in seed.location:
                min_loc = min(val.start, min_loc)
    return min_loc

print("part1: ", part1("d5input.txt"))
print("part2: ", part2("d5input.txt"))
