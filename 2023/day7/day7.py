import sys
from pathlib import Path
import re

sys.path.append(str(Path(__file__).parent.parent))
from aoc_utils import aoc_utils

INPUT = "day7-input.txt"
all_lines = aoc_utils.strip_newlines(aoc_utils.file_reader(INPUT))

from enum import Enum


class CardType(Enum):
    fiveKind = 7
    fourKind = 6
    fullHouse = 5
    threeKind = 4
    twoPair = 3
    onePair = 2
    highCard = 1

def rank_single_card(a, j_low = False):
    # Higher card has a LOWER index
    if j_low:
        vals = ['A', 'K', 'Q', 'T', '9', '8', '7', '6', '5', '4', '3', '2', "J"]
    else:
        vals = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
    return vals.index(a)

def card_type(card, part_two = False):
    """
        Five of a kind, where all five cards have the same label: AAAAA
        Four of a kind, where four cards have the same label and one card has a different label: AA8AA
        Full house, where three cards have the same label, and the remaining two cards share a different label: 23332
        Three of a kind, where three cards have the same label, and the remaining two cards are each different from any other card in the hand: TTT98
        Two pair, where two cards share one label, two other cards share a second label, and the remaining card has a third label: 23432
        One pair, where two cards share one label, and the other three cards have a different label from the pair and each other: A23A4
        High card, where all cards' labels are distinct: 23456
    """
    if not part_two or "J" not in card:
        # Try set approach first (works for five of a kind and high card)
        card_set = set([x for x in card])
        if len(card_set) == 1:
            # Five of a kind
            return CardType.fiveKind
        elif len(card_set) == 5:
            # High card
            return CardType.highCard

        # (Four of a kind, full house) and (three of a kind, and two pair) share set lengths
        u = {}
        for x in card:
            if x not in u.keys():
                u[x] = 1
            else:
                u[x] += 1
            if u[x] == 4:
                return CardType.fourKind

        for x in u.keys():
            if u[x] == 3 and len(u.keys()) == 3:
                # Three of a kind
                return CardType.threeKind
            elif u[x] == 3 and len(u.keys()) == 2:
                # Full house
                return CardType.fullHouse
            elif u[x] == 2 and len(u.keys()) == 4:
                # One pair
                return CardType.onePair
        return CardType.twoPair
    else:
        # Rank hand without J first
        stripped_hand = card.replace("J", "")
        number_js = card.count("J")

        # We add fake cards to ensure what we pass to card_type() is the right length
        fake_cards = ["B", "C", "D", "E", "F"]
        for i in range(number_js):
            stripped_hand += fake_cards[i]

        stripped_rank = card_type(stripped_hand)

        if number_js == 1:
            # Only impossible hands to find here are five kind, and full house
            if CardType.fourKind == stripped_rank:
                return CardType.fiveKind
            elif CardType.threeKind == stripped_rank:
                return CardType.fourKind
            elif CardType.twoPair == stripped_rank:
                return CardType.fullHouse
            elif CardType.onePair == stripped_rank:
                return CardType.threeKind
            elif CardType.highCard == stripped_rank:
                return CardType.onePair
        elif number_js == 2:
            # Impossible hands here are five kind, full house, four kind, and two pair
            if CardType.threeKind == stripped_rank:
                return CardType.fiveKind
            if CardType.onePair == stripped_rank:
                return CardType.fourKind
            if CardType.highCard == stripped_rank:
                return CardType.threeKind
        elif number_js == 3:
            # Only possible hands are one pair, of high card
            if CardType.onePair == stripped_rank:
                return CardType.fiveKind
            elif CardType.highCard == stripped_rank:
                return CardType.fourKind
        elif number_js == 4:
            if CardType.highCard == stripped_rank:
                return CardType.fiveKind
        else:
            return CardType.fiveKind


def card_win(card_one, card_two, part_two = False):
    ct_one = card_type(card_one,part_two)
    ct_two = card_type(card_two, part_two)

    if ct_one == ct_two:

        for i in range(len(card_one)):
            if rank_single_card(card_one[i], j_low=part_two) < rank_single_card(card_two[i], j_low=part_two):
                return True
            elif rank_single_card(card_one[i], j_low=part_two) > rank_single_card(card_two[i], j_low=part_two):
                return False
        return "failed"
    else:
        return ct_one.value > ct_two.value

def test():
    print(card_type("AAAAA"))
    print(card_type("AA8AA"))
    print(card_type("23332"))
    print(card_type("TTT98"))
    print(card_type("23432"))
    print(card_type("A23A4"))
    print(card_type("23456"))
    print(card_win("23456", "23456"))
    print(card_win("65432", "23456"))
    print(card_win("65432", "22456"))
    print(card_win("AAAA8", "AAAA9"))
    print(card_win("QQQ2A", "QQQJA", part_two=True))

class Hands:
    # Need the lt_gt functions to sort on
    hand = ""
    bid = 0
    part_two = False

    def __init__(self, h, b, part_two=False):
        self.hand = h
        self.bid = int(b)
        self.part_two = part_two

    def __gt__(self, other):
        return card_win(self.hand, other.hand, part_two=self.part_two)

def hand_ranking(debug=False, part_two = False):
    h_list = []
    for l in all_lines:
        hand, bid = l.split(" ")
        h_list.append(Hands(hand,bid, part_two))

    sum = 0
    max_rank = len(h_list)
    sorted_hands = sorted(h_list)
    for i in range(max_rank):
        if debug:
            print(sorted_hands[i].hand)
            print(sorted_hands[i].bid * (i+1))
        sum += sorted_hands[i].bid * (i+1)
    return sum

print("2023 day 7 part 1 Sum is %d" % hand_ranking())
print("2023 day 7 part 2 Sum is %d" % hand_ranking(part_two=True))
