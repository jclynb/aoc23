from functools import cmp_to_key
class Hand:
    def __init__(self, hand, bid):
        self.hand = hand
        self.unique_vals = set(hand)
        self.bid = int(bid)
        self.jokernum = self.hand.count('J')
        self.rank = self.get_rank()
    
    def get_rank(self):
        # Check for five of a kind
        if len(self.unique_vals) == 1:
            return 6
        # Check for four of a kind
        elif len(self.unique_vals) == 2 and (self.hand.count(self.hand[0]) == 1 or self.hand.count(self.hand[0]) == 4):
            if self.jokernum:
                return 6
            else:
                return 5
        # Check for full house
        elif len(self.unique_vals) == 2:
            if self.jokernum:
                return 6
            else:
                return 4
        # Check for three of a kind
        elif any(self.hand.count(val) == 3 for val in self.unique_vals):
            if self.jokernum:
                return 5
            else:
                return 3
        # Check for two pair (ex: [5 5 6 6 8] -> set(5 6 8))
        elif len(self.unique_vals) == 3:
            if self.jokernum == 2:
                return 5
            elif self.jokernum == 1:
                return 4
            else:
                return 2
        # Check for one pair
        elif len(self.unique_vals) == 4:
            if self.jokernum:
                return 3
            else:
                return 1
        # Else high card
        else:
            if self.jokernum:
                return 1
            else:
                return 0
            
def get_sorted_hands(input):
    hands = []
    lines = open(input, "r")
    for line in lines.readlines():
        hand, bid = line.split()
        hands.append(Hand(hand, bid))
    return sorted(hands, key=cmp_to_key(compare_ranks_then_hands))

def compare_ranks_then_hands(a, b):
    def compare_hands(a, b):
        val_map = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 1, 'Q': 12, 'K': 13, 'A': 14}
        """ Breaks a tie between two hands `a` and `b` where each is of the same
        rank (four of a kind, full house, etc.) by seeing which hand has the
        higher valued cards. Returns 1 when `a` wins, 0 in the case of a true
        tie, and -1 when `b` wins. """
        for a_element, b_element in zip(a, b):
            if val_map[a_element] > val_map[b_element]:
                return 1
            elif val_map[a_element] < val_map[b_element]:
                return -1
        return 0
    # Compare Ranks First
    if a.rank > b.rank:
        return 1
    elif a.rank < b.rank:
        return -1
    else:
        return compare_hands(a.hand, b.hand)

def calc_winnings(hands):
    total = 0
    for i, hand in enumerate(hands):
        total += (i + 1)*hand.bid
    return total 

print("part1: ", calc_winnings(get_sorted_hands("d7input.txt")))