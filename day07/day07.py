from enum import Enum

card_label = {
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6' : 6,
    '7' : 7,
    '8' : 8,
    '9' : 9,
    'T' : 10,
    'J' : 11,
    'Q' : 12,
    'K' : 13,
    'A' : 14
}

card_label_joker = {
    'J': 2,
    '2': 3,
    '3': 4,
    '4': 5,
    '5': 6,
    '6' : 7,
    '7' : 8,
    '8' : 9,
    '9' : 10,
    'T' : 11,
    'Q' : 12,
    'K' : 13,
    'A' : 14
}

class CardType(Enum):
    HIGH_CARD = 1
    PAIR = 2
    TWO_PAIR = 3
    THREE_OF_A_KIND = 4
    FULL_HOUSE = 5
    FOUR_OF_A_KIND = 6
    FIVE_OF_A_KIND = 7

    def __lt__(self, other):
        return self.value < other.value


class Play():
    def __init__(self, hand: str, bid: int, joker=False):
        self.hand = hand
        self.bid = bid
        self.type = self.get_type(joker)
        self.rank = 0
        self.joker = joker
    
    def get_type(self, joker=False) -> CardType:
        found_cards = {}
        for card in self.hand:
            if card in found_cards:
                found_cards[card] += 1
            else:
                found_cards[card] = 1
        
        if joker:
            return self.__get_type_with_joker(found_cards)
        else:
            return self.__get_card_type(found_cards)
    
    def __get_type_with_joker(self, found_cards: dict) -> CardType:
        found_cards_copy = found_cards.copy()

        if 'J' in found_cards_copy and found_cards_copy['J'] != 5:
            joker_amount = found_cards_copy['J']
            found_cards_copy.pop('J')
            sorted_cards = [k for k, _ in sorted(found_cards_copy.items(), key=lambda item: item[1], reverse=True)]
            found_cards_copy[sorted_cards[0]] += joker_amount

        return self.__get_card_type(found_cards_copy)

    def __get_card_type(self, found_cards: dict) -> CardType:
        if len(found_cards) == 5:
            return CardType.HIGH_CARD
        elif len(found_cards) == 4:
            return CardType.PAIR
        elif len(found_cards) == 3:
            if 3 in found_cards.values():
                return CardType.THREE_OF_A_KIND
            else:
                return CardType.TWO_PAIR
        elif len(found_cards) == 2:
            if 2 in found_cards.values():
                return CardType.FULL_HOUSE
            else:
                return CardType.FOUR_OF_A_KIND
        else:
            return CardType.FIVE_OF_A_KIND

    
    def set_rank(self, rank: int):
        self.rank = rank
    
    def __lt__(self, other):
        if self.joker:
            label = card_label_joker
        else:
            label = card_label

        if self.type == other.type:
            for i in range(5):
                if label[self.hand[i]] == label[other.hand[i]]:
                    continue
                else:
                    return label[self.hand[i]] < label[other.hand[i]]
        else:
            return self.type < other.type
    
    def __str__(self) -> str:
        return f'{self.hand} {self.bid} {self.type} {self.rank}'

class BidsParser():
    @staticmethod
    def parse(file_string: str, joker=False):
        with open(file_string, 'r') as open_file:
            hands_and_bids = open_file.readlines()

        plays = []
        for hand_and_bid in hands_and_bids:
            hand, bid = hand_and_bid.split(' ')
            plays.append(Play(hand, int(bid), joker))
        
        return plays
    
# Part 1
plays = BidsParser.parse('day07/bids.txt')
sorted_plays = sorted(plays)
for i in range(1, len(sorted_plays) + 1):
    sorted_plays[i - 1].set_rank(i)

print(sum([play.bid * play.rank for play in sorted_plays]))

# Part 2
plays = BidsParser.parse('day07/bids.txt', True)
sorted_plays = sorted(plays)
for i in range(1, len(sorted_plays) + 1):
    sorted_plays[i - 1].set_rank(i)

print(sum([play.bid * play.rank for play in sorted_plays]))
