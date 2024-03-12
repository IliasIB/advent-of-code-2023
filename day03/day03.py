import numpy
from functools import reduce

class GearsParser():
    @staticmethod
    def parse_gears(file_string):
        open_file = open(file_string, 'r')
        gears_strings = open_file.readlines()
        open_file.close()

        gears_matrix = []
        for gears_string in gears_strings:
            gears_matrix.append([*gears_string.replace('\n', '')])
        return gears_matrix
    
    @staticmethod
    def gear_mark_directions(gears_matrix, gear_marks, x, y, x_offset, y_offset):
        try:
            if gears_matrix[y + y_offset][x + x_offset].isnumeric() and not gear_marks[y + y_offset][x + x_offset]:
                gear_marks[y + y_offset][x + x_offset] = True
                GearsParser.gear_mark_directions(gears_matrix, gear_marks, x + x_offset, y + y_offset, 1, 0)
                GearsParser.gear_mark_directions(gears_matrix, gear_marks, x + x_offset, y + y_offset, -1, 0)
        except IndexError:
            pass
    
    @staticmethod
    def get_gear_marks(gears_matrix):
        gear_marks = numpy.full((len(gears_matrix), len(gears_matrix[0])), False)
        directions = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]

        for y in range(len(gears_matrix)):
            for x in range(len(gears_matrix[0])):
                if not gears_matrix[y][x].isalnum() and gears_matrix[y][x] != '.':
                    for direction in directions:
                        GearsParser.gear_mark_directions(
                            gears_matrix,
                            gear_marks,
                            x, y,
                            *direction
                        )
        return gear_marks
    
    @staticmethod
    def get_gear_count(gears_matrix, gear_marks):
        gear_count = 0
        for y in range(len(gears_matrix)):
            current_number = ''
            for x in range(len(gears_matrix[0])):
                if gears_matrix[y][x].isnumeric() and gear_marks[y][x]:
                    current_number += gears_matrix[y][x]
                    if x == len(gears_matrix[0]) - 1:
                        gear_count += int(current_number)
                elif current_number != '':
                    gear_count += int(current_number)
                    current_number = ''
        return gear_count
    
    @staticmethod
    def get_gear_neighbour_count(gears_matrix, x, y):
        count = 0
        directions = [(1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
        for direction in directions:
            try:
                if gears_matrix[y + direction[1]][x + direction[0]].isnumeric():
                    count += 1
            except IndexError:
                pass
        return count
    
    @staticmethod
    def get_gear_neighbour(gears_matrix, marks, x, y):
        try:
            neighbour = ''
            if gears_matrix[y][x].isnumeric() and not marks[y][x]:
                marks[y][x] = True
                neighbour = (
                    GearsParser.get_gear_neighbour(gears_matrix, marks, x - 1, y) +
                    gears_matrix[y][x] +
                    GearsParser.get_gear_neighbour(gears_matrix, marks, x + 1, y)
                )
            return neighbour
        except IndexError:
            return ''
    
    @staticmethod
    def get_gear_neighbours(gears_matrix, x, y):
        neighbours = []
        marks = numpy.full((len(gears_matrix), len(gears_matrix[0])), False)
        directions = [(1, -1), (0, -1), (-1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
        for direction in directions:
            try:
                if gears_matrix[y + direction[1]][x + direction[0]].isnumeric() and not marks[y + direction[1]][x + direction[0]]:
                    neighbours.append(int(GearsParser.get_gear_neighbour(gears_matrix, marks, x + direction[0], y + direction[1])))
            except IndexError:
                pass
        return neighbours
    
    @staticmethod
    def get_gear_ratios(gears_matrix):
        gear_ratios = []
        for y in range(len(gears_matrix)):
            for x in range(len(gears_matrix[0])):
                if gears_matrix[y][x] == '*':
                    neighbours = GearsParser.get_gear_neighbours(gears_matrix, x, y)
                    if len(neighbours) == 2:
                        gear_ratios.append(reduce(lambda x, y: x * y, neighbours))
        return gear_ratios

# Part 1
gears_matrix = GearsParser.parse_gears('gears.txt')
gear_marks = GearsParser.get_gear_marks(gears_matrix)
print(GearsParser.get_gear_count(gears_matrix, gear_marks))

# Part 2
gears_matrix = GearsParser.parse_gears('gears.txt')
gear_ratios = GearsParser.get_gear_ratios(gears_matrix)
print(sum(gear_ratios))