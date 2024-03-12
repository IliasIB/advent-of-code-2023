import re
from queue import Queue

class Card():
    def __init__(self, id, winning_numbers, numbers):
        self.numbers = numbers
        self.winning_numbers = winning_numbers
        self.id = id

    @classmethod
    def parse(cls, card_string):
        card_string_splitted = card_string.replace('\n', '').split(' | ')

        # Gets the numbers from the second part of the card string
        numbers = list(map(int, re.findall(r'\d+', card_string_splitted[1])))

        # Gets the winning numbers from the first part of the card string
        winning_numbers = list(map(int, re.findall(r'\d+', card_string_splitted[0].split(': ')[1])))

        id = int(re.search(r'\d+', card_string_splitted[0].split(': ')[0]).group())

        return cls(id, winning_numbers, numbers)
    
    def get_points(self):
        points = 0
        for number in self.numbers:
            if number in self.winning_numbers and points == 0:
                points = 1
            elif number in self.winning_numbers:
                points *= 2
        return points
    
    def get_matching_numbers(self):
        return len([number for number in self.numbers if number in self.winning_numbers])

class CardsParser():
    @staticmethod
    def parse(file_string):
        with open(file_string, 'r') as open_file:
            card_strings = open_file.readlines()

        cards = {}
        for i, card_string in enumerate(card_strings, 1):
            cards[i] = Card.parse(card_string.replace('\n', ''))

        return cards
    
    @staticmethod
    def get_points(cards):
        points = 0
        for card in cards.values():
            points += card.get_points()
        return points
    
    @staticmethod
    def solve_cards(cards):
        card_amount = len(cards)
        matching_numbers = {}
        queue = Queue()
        for card in cards.values():
            matching_numbers[card.id] = card.get_matching_numbers()
            queue.put((card.id, matching_numbers[card.id]))

        while queue.qsize() > 0:
            card = queue.get()                
            for i in range(1, card[1] + 1):
                card_amount += 1
                new_card_id = min(len(cards) - 1, card[0] + i)
                queue.put((new_card_id, matching_numbers[new_card_id]))
        return card_amount

# Part 1
cards = CardsParser.parse('cards.txt')
print(CardsParser.get_points(cards))

# Part 2
cards = CardsParser.parse('cards.txt')
print(CardsParser.solve_cards(cards))