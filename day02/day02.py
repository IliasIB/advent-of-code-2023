from functools import reduce

class Round():
    def __init__(self, round_string):
        self.colors = {}
        round_string_split = round_string.split(', ')
        for color in round_string_split:
            color_split = color.split(' ')
            try:
                self.colors[color_split[1]] += int(color_split[0])
            except KeyError:
                self.colors[color_split[1]] = int(color_split[0])
    
    def is_valid(self, colors):
        for color in self.colors:
            try:
                if self.colors[color] > colors[color]:
                    return False
            except KeyError:
                return False
        return True


class Game():
    def __init__(self, game_string):
        self.rounds = []
        game_string_split = game_string.split(': ')
        self.id = int(game_string_split[0].split(' ')[1])
        rounds_string = game_string_split[1].split('; ')
        for round_string in rounds_string:
            round = Round(round_string)
            self.rounds.append(round)
    
    def is_valid(self, colors):
        for round in self.rounds:
            if not round.is_valid(colors):
                return False
        return True
    
    def fewest_possible(self):
        colors = {}
        for round in self.rounds:
            for color in round.colors:
                try:
                    if round.colors[color] > colors[color]:
                        colors[color] = round.colors[color]
                except KeyError:
                    colors[color] = round.colors[color]
        return colors

class GameParser():
    @staticmethod
    def parse_games(file_string):
        open_file = open(file_string, 'r')
        games_strings = open_file.readlines()
        open_file.close()

        games = []
        for game_string in games_strings:
            game = Game(game_string.replace('\n', ''))
            games.append(game)
        return games

class Utils():
    @staticmethod
    def power_set(set):
        return reduce((lambda x, y: x * y), set)


# Part 1
games = GameParser.parse_games('games.txt')
valid_game_ids = [ game.id for game in games if game.is_valid({ 'blue': 14, 'red': 12, 'green': 13 }) ]
print(sum(valid_game_ids))

# Part 2
games = GameParser.parse_games('games.txt')
fewest_colors = [ game.fewest_possible() for game in games]
power_sets = list(map(lambda x: Utils.power_set(x.values()), fewest_colors))
print(sum(power_sets))
