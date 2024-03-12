import re
import math
from functools import reduce

class TimeDistanceParser():
    @staticmethod
    def parse(file_string):
        with open(file_string, 'r') as open_file:
            times_and_distances = open_file.readlines()
        
        times = list(map(int, re.findall(r'\d+', times_and_distances[0])))
        distances = list(map(int, re.findall(r'\d+', times_and_distances[1])))

        return times, distances
    
    @staticmethod
    def calculate_possible_presses(times, distances):
        possible_presses = []
        for time, distance in zip(times, distances):
            press_1 = math.ceil(((time + math.sqrt(time ** 2 - 4 * distance)) / 2) - 1)
            press_2 = math.floor(((time - math.sqrt(time ** 2 - 4 * distance)) / 2) + 1)
            possible_presses.append(press_1 - press_2 + 1)
        return possible_presses
    
# Part 1
times, distances = TimeDistanceParser.parse('day06/times.txt')
possible_presses = TimeDistanceParser.calculate_possible_presses(times, distances)
print(reduce(lambda x, y: x * y, possible_presses))

# Part 2
times, distances = TimeDistanceParser.parse('day06/times2.txt')
possible_presses = TimeDistanceParser.calculate_possible_presses(times, distances)
print(reduce(lambda x, y: x * y, possible_presses))