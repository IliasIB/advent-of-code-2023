"""Day 10 Puzzle"""
from dataclasses import dataclass
from enum import Enum
from queue import Queue
from shapely.geometry import point
from shapely.geometry.polygon import Polygon

class PipeType(Enum):
    """Represents the type of pipe."""
    NORTH_SOUTH = 0
    EAST_WEST = 1
    NORTH_EAST = 2
    NORTH_WEST = 3
    SOUTH_WEST = 4
    SOUTH_EAST = 5
    GROUND = 6
    STARTING_POSITION = 7

    def is_north_type(self):
        """Returns whether the pipe is a north type."""
        return self in [
            PipeType.NORTH_SOUTH,
            PipeType.NORTH_EAST,
            PipeType.NORTH_WEST,
            PipeType.STARTING_POSITION
        ]

    def is_south_type(self):
        """Returns whether the pipe is a south type."""
        return self in [
            PipeType.SOUTH_WEST,
            PipeType.SOUTH_EAST,
            PipeType.NORTH_SOUTH,
            PipeType.STARTING_POSITION
        ]

    def is_east_type(self):
        """Returns whether the pipe is a east type."""
        return self in [
            PipeType.EAST_WEST,
            PipeType.NORTH_EAST,
            PipeType.SOUTH_EAST,
            PipeType.STARTING_POSITION
        ]

    def is_west_type(self):
        """Returns whether the pipe is a west type."""
        return self in [
            PipeType.EAST_WEST,
            PipeType.NORTH_WEST,
            PipeType.SOUTH_WEST,
            PipeType.STARTING_POSITION
        ]

@dataclass
class Pipe():
    """Represents a pipe."""
    position: tuple[int, int]
    pipe_type: PipeType

    def __repr__(self):
        return f'Pipe({self.position}, {self.pipe_type})'

class PipeParser():
    """Parses a file into a list of pipes."""
    @staticmethod
    def parse(file_string: str):
        """Parses a file into a list of pipes."""
        with open(file_string, 'r', encoding="utf-8") as open_file:
            pipe_strings = list(map(lambda x: x.replace('\n', ''), open_file.readlines()))

        pipes = []
        starting_point = None
        for i, pipe_string in enumerate(pipe_strings):
            pipes_row = []
            for j, pipe_char in enumerate(pipe_string):
                pipe_type = PipeParser.__get_pipe_type(pipe_char)
                pipes_row.append(Pipe((j, i), pipe_type))
                if pipe_type == PipeType.STARTING_POSITION:
                    starting_point = (j, i)
            pipes.append(pipes_row)
        return pipes, starting_point

    @staticmethod
    def __get_pipe_type(pipe_char):
        match pipe_char:
            case '.':
                pipe_type = PipeType.GROUND
            case '|':
                pipe_type = PipeType.NORTH_SOUTH
            case '-':
                pipe_type = PipeType.EAST_WEST
            case 'L':
                pipe_type = PipeType.NORTH_EAST
            case 'J':
                pipe_type = PipeType.NORTH_WEST
            case '7':
                pipe_type = PipeType.SOUTH_WEST
            case 'F':
                pipe_type = PipeType.SOUTH_EAST
            case 'S':
                pipe_type = PipeType.STARTING_POSITION
        return pipe_type

    @staticmethod
    def __get_connections(
        pipes: list[list[Pipe]],
    ) -> list[tuple[int, int]]:
        """Gets the connections for each pipe."""
        connections = {}
        max_x, max_y = len(pipes[0]), len(pipes)

        for y, pipes_row in enumerate(pipes):
            for x, pipe in enumerate(pipes_row):
                pipe_connections = []
                if pipe.pipe_type.is_north_type():
                    if y - 1 >= 0 and pipes[y - 1][x].pipe_type.is_south_type():
                        pipe_connections.append((x, y - 1))
                if pipe.pipe_type.is_south_type():
                    if y + 1 < max_y and pipes[y + 1][x].pipe_type.is_north_type():
                        pipe_connections.append((x, y + 1))
                if pipe.pipe_type.is_east_type():
                    if x + 1 < max_x and pipes[y][x + 1].pipe_type.is_west_type():
                        pipe_connections.append((x + 1, y))
                if pipe.pipe_type.is_west_type():
                    if x - 1 >= 0 and pipes[y][x - 1].pipe_type.is_east_type():
                        pipe_connections.append((x - 1, y))
                connections[(x, y)] = pipe_connections
        return connections

    @staticmethod
    def find_farthest_step_amount(pipes, starting_point):
        """Finds a cycle in the connections using recursive depth first search."""
        queue = Queue()
        queue.put((starting_point, None))
        connections = PipeParser.__get_connections(pipes)
        # visited = PipeParser.__get_empty_visited(len(pipes[0]), len(pipes))
        steps = {}
        steps[starting_point] = 0

        while not queue.empty():
            current, parent = queue.get()

            for connection in connections[current]:
                if connection == parent or steps.get(connection) is not None:
                    continue

                steps[connection] = steps[current] + 1
                queue.put((connection, current))

        return max(steps.values())

    @staticmethod
    def __get_polygon(pipes, starting_point):
        """Gets the polygon."""
        connections = PipeParser.__get_connections(pipes)
        path = [starting_point]
        current = starting_point
        parent = None
        while parent is None or current != starting_point:
            for connection in connections[current]:
                if connection == parent:
                    continue
                path.append(connection)
                parent = current
                current = connection
                break
            else:
                break
        return Polygon(path)

    @staticmethod
    def get_enclosed_points(pipes, starting_point):
        """Gets the enclosed points."""
        polygon = PipeParser.__get_polygon(pipes, starting_point)
        enclosed_points = []
        for y, pipes_row in enumerate(pipes):
            for x, pipe in enumerate(pipes_row):
                if (
                    polygon.contains(point.Point(*pipe.position))
                ):
                    enclosed_points.append((x, y))
        return enclosed_points

# Part 1
def part1():
    """Part 1."""
    pipes, starting_point = PipeParser.parse('day10/pipes.txt')
    cycle = PipeParser.find_farthest_step_amount(pipes, starting_point)
    print(cycle)

part1()

# Part 2
def part2():
    """Part 2."""
    pipes, starting_point = PipeParser.parse('day10/pipes.txt')
    enclosed_points = PipeParser.get_enclosed_points(pipes, starting_point)
    print(len(enclosed_points))

part2()
