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

def rank_single_card(a):
    # Higher card has a LOWER index
    vals = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
    return vals.index(a)

def card_type(card):
    """
        Five of a kind, where all five cards have the same label: AAAAA
        Four of a kind, where four cards have the same label and one card has a different label: AA8AA
        Full house, where three cards have the same label, and the remaining two cards share a different label: 23332
        Three of a kind, where three cards have the same label, and the remaining two cards are each different from any other card in the hand: TTT98
        Two pair, where two cards share one label, two other cards share a second label, and the remaining card has a third label: 23432
        One pair, where two cards share one label, and the other three cards have a different label from the pair and each other: A23A4
        High card, where all cards' labels are distinct: 23456
    """

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

def card_win(card_one, card_two):
    ct_one = card_type(card_one)
    ct_two = card_type(card_two)
    if ct_one == ct_two:

        for i in range(len(card_one)):
            if rank_single_card(card_one[i]) < rank_single_card(card_two[i]):
                return True
            elif rank_single_card(card_one[i]) > rank_single_card(card_two[i]):
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

class Hands:
    # Need the lt_gt functions to sort on
    hand = ""
    bid = 0

    def __init__(self, h, b):
        self.hand = h
        self.bid = int(b)

    def __gt__(self, other):
        return card_win(self.hand, other.hand)

h_list = []
for l in all_lines:
    hand, bid = l.split(" ")
    h_list.append(Hands(hand,bid))

sum = 0
max_rank = len(h_list)
sorted_hands = sorted(h_list)
for i in range(max_rank):
    print(sorted_hands[i].hand)
    print(sorted_hands[i].bid * (i+1))
    sum += sorted_hands[i].bid * (i+1)
print("Sum is %d" % sum)

