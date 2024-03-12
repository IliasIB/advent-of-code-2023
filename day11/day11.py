"""Day 11 Puzzle"""
class GalaxyParser():
    """Parses a file into a list of galaxies."""
    @staticmethod
    def parse(file_string: str):
        """Parses a file into a list of galaxies."""
        with open(file_string, 'r', encoding="utf-8") as open_file:
            galaxy_strings = list(map(lambda x: x.replace('\n', ''), open_file.readlines()))

        galaxies = {}
        y = 0
        galaxy_number = 1
        for galaxy_string in galaxy_strings:
            if galaxy_string == len(galaxy_string) * galaxy_string[0]:
                y += 2
            else:
                for x, galaxy_char in enumerate(galaxy_string):
                    if galaxy_char == '#':
                        galaxies[galaxy_number] = (x, y)
                        galaxy_number += 1
                y += 1
        return galaxies

    @staticmethod
    def calculate_distances(galaxies):
        """Calculates the distances between galaxies."""
        distances = {}
        for key1 in galaxies:
            for key2 in galaxies:
                if (
                    key1 != key2 and
                    (key1, key2) not in distances and
                    (key2, key1) not in distances
                ):
                    distances[(key1, key2)] = (
                        abs(galaxies[key1][0] - galaxies[key2][0]) +
                        abs(galaxies[key1][1] - galaxies[key2][1])
                    )
        return distances

def part1():
    """Part 1"""
    galaxies = GalaxyParser.parse('day11/example.txt')
    distances = GalaxyParser.calculate_distances(galaxies)
    print(sum(distances.values()))

# Part 1
part1()
