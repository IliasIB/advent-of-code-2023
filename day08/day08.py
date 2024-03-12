import re
import math

class MapParser():
    @staticmethod
    def parse(file_string: str, joker=False):
        with open(file_string, 'r') as open_file:
            directions_and_paths = open_file.readlines()

        directions = directions_and_paths[0].replace('\n', '')
        starting_nodes = []
        right = {}
        left = {}
        for path_string in directions_and_paths[2:]:
            paths = re.findall(r'[A-Z]+', path_string)
            if paths[0].endswith('A'):
                starting_nodes.append(paths[0])

            left[paths[0]] = paths[1]
            right[paths[0]] = paths[2]
        
        return left, right, directions, starting_nodes
    
    @staticmethod
    def get_step_amount(directions: list, left: dict, right: dict, initial = 'AAA', full=True) -> int:
        steps = 0
        current = initial
        while not MapParser.is_end_node(current, full):
            if directions[steps % len(directions)] == 'R':
                current = right[current]
            else:
                current = left[current]
            steps += 1
        
        return steps
    
    @staticmethod
    def is_end_node(node: str, full=True) -> bool:
        if full:
            return node == 'ZZZ'
        else:
            return node.endswith('Z')
    
    @staticmethod
    def get_ghost_step_amount(directions: list, left: dict, right: dict, starting_nodes: list) -> int:
        steps = list(map(lambda x: MapParser.get_step_amount(directions, left, right, x, False), starting_nodes))
        return math.lcm(*steps)

# Part 1
left, right, directions, _ = MapParser.parse('day08/map.txt')
step_amount = MapParser.get_step_amount(directions, left, right)
print(f'Part 1: {step_amount}')

# Part 2
left, right, directions, starting_nodes = MapParser.parse('day08/map.txt')
step_amount = MapParser.get_ghost_step_amount(directions, left, right, starting_nodes)
print(f'Part 2: {step_amount}')