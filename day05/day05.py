class SeedMappingParser():
    @staticmethod
    def parse(file_string):
        with open(file_string, 'r') as open_file:
            seeds_and_mappings = open_file.readlines()

        seeds = list(map(int, seeds_and_mappings[0].split(': ')[1].split(' ')))
        mappings = seeds_and_mappings[2:]
        return seeds, mappings
    
    @staticmethod
    def parse_with_range(file_string):
        with open(file_string, 'r') as open_file:
            seeds_and_mappings = open_file.readlines()

        seeds = list(map(int, seeds_and_mappings[0].split(': ')[1].split(' ')))
        seeds_with_range = []
        for i in range(0, len(seeds), 2):
            seeds_with_range.append((seeds[i], seeds[i + 1]))

        mappings = seeds_and_mappings[2:]
        return seeds_with_range, mappings
    
    @staticmethod
    def get_locations(seeds, mappings):
        pointer = 1
        current_results = []
        previous_results = seeds.copy()
        while pointer < len(mappings):
            while pointer < len(mappings) and mappings[pointer] != '\n':
                destination, source, ranges = list(map(int, mappings[pointer].replace('\n', '').split(' ')))
                for previous_result in previous_results.copy():
                    position = previous_result - source
                    if position >= 0 and position < ranges:
                        current_results.append(destination + position)
                        previous_results.remove(previous_result)
                pointer += 1
            for previous_result in previous_results:
                current_results.append(previous_result)
            previous_results = current_results.copy()
            current_results = []
            pointer += 2
        
        return previous_results
    
    @staticmethod
    def get_locations_with_range(seeds, mappings):
        pointer = 1
        current_results = []
        previous_results = seeds.copy()
        while pointer < len(mappings):
            while pointer < len(mappings) and mappings[pointer] != '\n':
                destination, source, ranges = list(map(int, mappings[pointer].replace('\n', '').split(' ')))
                for previous_result in previous_results.copy():
                    # Case 1: left in range, right out of range
                    if source <= previous_result[0] <= source + ranges < previous_result[0] + previous_result[1]:
                        position = previous_result[0] - source
                        new_range_1 = source + ranges - previous_result[0]
                        new_range_2 = previous_result[1] - new_range_1

                        current_results.append((destination + position, new_range_1))
                        previous_results.append((source + ranges, new_range_2))
                        previous_results.remove(previous_result)
                    # Case 2: left out of range, right in range
                    elif previous_result[0] < source <= previous_result[0] + previous_result[1] <= source + ranges:
                        new_range_1 = previous_result[0] + previous_result[1] - source
                        new_range_2 = previous_result[1] - new_range_1

                        current_results.append((destination, new_range_1))
                        previous_results.append((previous_result[0], new_range_2))
                        previous_results.remove(previous_result)
                    # Case 3: left out of range, right out of range
                    elif previous_result[0] < source < source + ranges < previous_result[0] + previous_result[1]:
                        new_range_left = source - previous_result[0]
                        new_range_right = (previous_result[0] + previous_result[1]) - (source + ranges)

                        current_results.append((destination, ranges))
                        previous_results.append((previous_result[0], new_range_left))
                        previous_results.append((source + ranges, new_range_right))
                        previous_results.remove(previous_result)
                    # Case 4: left in range, right in range
                    elif source <= previous_result[0] < previous_result[0] + previous_result[1] <= source + ranges:
                        position = previous_result[0] - source
                        current_results.append((destination + position, previous_result[1]))
                        previous_results.remove(previous_result)
                pointer += 1
            for previous_result in previous_results:
                current_results.append(previous_result)
            previous_results = current_results.copy()
            current_results = []
            pointer += 2
        
        return previous_results

# Part 1
seeds, mappings = SeedMappingParser.parse('day05/seeds.txt')
locations = SeedMappingParser.get_locations(seeds, mappings)
print(min(locations))

# Part 2
seeds_with_range, mappings = SeedMappingParser.parse_with_range('day05/seeds.txt')
locations = SeedMappingParser.get_locations_with_range(seeds_with_range, mappings)
print(locations)
print(min([location[0] for location in locations]))