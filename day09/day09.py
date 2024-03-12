class HistoryParser():
    @staticmethod
    def parse(file_string: str):
        with open(file_string, 'r') as open_file:
            history_strings = open_file.readlines()

        histories = []
        for history_string in history_strings:
            histories.append(list(map(int, history_string.split(' '))))
        return histories

    @staticmethod
    def get_next_number(history: list) -> int:
        current_numbers = []
        if all(p == 0 for p in history):
            return 0
        for i in range(1, len(history)):
            current_numbers.append(history[i] - history[i - 1])
        return history[-1] + HistoryParser.get_next_number(current_numbers)
    
    @staticmethod
    def get_previous_number(history: list) -> int:
        current_numbers = []
        if all(p == 0 for p in history):
            return 0
        for i in range(1, len(history)):
            current_numbers.append(history[i] - history[i - 1])
        return history[0] - HistoryParser.get_previous_number(current_numbers)

# 1   3   6  10  15  21  28
#   2   3   4   5   6   7
#     1   1   1   1   1
#       0   0   0   0

# Part 1
histories = HistoryParser.parse('day09/history.txt')
history_numbers = list(map(lambda x: HistoryParser.get_next_number(x), histories))
print(f'Part 1: {sum(history_numbers)}')

# Part 2
histories = HistoryParser.parse('day09/history.txt')
history_numbers = list(map(lambda x: HistoryParser.get_previous_number(x), histories))
print(f'Part 2: {sum(history_numbers)}')